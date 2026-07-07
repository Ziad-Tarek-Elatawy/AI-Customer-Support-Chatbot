import os
import time
import logging
from dataclasses import dataclass, field

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RETRIEVAL_K = 5
RELEVANCE_THRESHOLD = 0.25

GREETINGS = {"hi", "hello", "hey", "good morning", "good evening", "good afternoon", "sup", "yo", "hola", "greetings"}

SYSTEM_PROMPT = (
    "You are a professional, friendly AI Customer Support Assistant.\n\n"
    "RULES:\n"
    "- Never reveal your internal thinking or reasoning process. Always respond directly to the user.\n"
    "- Never start your response with phrases like 'Okay, the user is asking...' or 'Let me check...'\n\n"
    "HOW TO ANSWER:\n"
    "1. If the context below contains relevant information, use it to give an accurate answer.\n"
    "2. If the context is partially relevant, use what's available and supplement with helpful general guidance.\n"
    "3. If the context has nothing relevant, use your general knowledge to help the user as best you can.\n"
    "4. Only if the question is completely outside customer support, politely let them know and suggest topics you CAN help with:\n"
    "   - Orders (tracking, cancellation, status)\n"
    "   - Refunds & returns\n"
    "   - Account management\n"
    "   - Payments & billing\n"
    "   - Shipping & delivery\n"
    "   - Subscriptions\n"
    "   - Invoices\n\n"
    "RESPONSE FORMAT:\n"
    "- Use numbered steps for procedures.\n"
    "- Use bullet points for lists.\n"
    "- Replace placeholders like {{Order Number}} by politely asking the user to provide that value.\n"
    "- Be concise and helpful — no filler text.\n\n"
    "Context:\n{context}"
)


@dataclass
class RAGResult:
    answer: str
    sources: list[dict] = field(default_factory=list)
    confidence: float = 0.0


class CustomerSupportRAG:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        chroma_dir = os.path.join(base_dir, "data", "chroma_db")

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENROUTER_API_KEY is not set in environment variables")

        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

        self.vector_store = Chroma(
            persist_directory=chroma_dir,
            embedding_function=self.embeddings,
        )

        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model="nvidia/nemotron-3-super-120b-a12b:free",
            temperature=0.1,
            max_tokens=1024,
            timeout=30,
        )

        self.qa_chain = self._build_qa_chain()

    def _build_qa_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
        ])
        return create_stuff_documents_chain(self.llm, prompt)

    def _retrieve(self, query: str):
        """Retrieve documents with relevance scores and filter by threshold."""
        results = self.vector_store.similarity_search_with_relevance_scores(
            query, k=RETRIEVAL_K
        )
        return [(doc, score) for doc, score in results if score >= RELEVANCE_THRESHOLD]

    def get_response(self, user_query: str) -> RAGResult:
        user_query = user_query.strip()
        if not user_query:
            return RAGResult(answer="Please provide a question so I can help you.")

        if user_query.lower().rstrip("!?.") in GREETINGS:
            return RAGResult(
                answer="Hello! Welcome to our support. How can I help you today?",
                confidence=1.0,
            )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                docs_with_scores = self._retrieve(user_query)

                if docs_with_scores:
                    context_docs = [doc for doc, _ in docs_with_scores]
                    avg_score = sum(s for _, s in docs_with_scores) / len(docs_with_scores)
                else:
                    from langchain_core.documents import Document
                    context_docs = [Document(page_content="No relevant information found in the knowledge base.")]
                    avg_score = 0.0

                answer = self.qa_chain.invoke({
                    "input": user_query,
                    "context": context_docs,
                })

                sources = []
                for doc, score in docs_with_scores:
                    sources.append({
                        "content": doc.page_content[:200],
                        "category": doc.metadata.get("category", ""),
                        "intent": doc.metadata.get("intent", ""),
                        "score": round(score, 3),
                    })

                return RAGResult(
                    answer=answer,
                    sources=sources,
                    confidence=round(avg_score, 2),
                )

            except Exception as e:
                error_str = str(e)
                is_retryable = any(code in error_str for code in ("429", "500", "502", "503"))

                if is_retryable and attempt < max_retries - 1:
                    wait = 10 * (attempt + 1)
                    logger.warning("Retryable error (attempt %d/%d), waiting %ds: %s",
                                   attempt + 1, max_retries, wait, error_str)
                    time.sleep(wait)
                    continue

                if "429" in error_str or "rate" in error_str.lower():
                    logger.warning("Rate limited after %d attempts", attempt + 1)
                    return RAGResult(answer="The service is busy right now. Please try again in a few seconds.")

                logger.error("RAG pipeline error: %s", error_str)
                return RAGResult(answer="Something went wrong while processing your question. Please try again.")

        return RAGResult(answer="Unable to process your request after multiple attempts. Please try again later.")


_rag_instance: CustomerSupportRAG | None = None


def _get_instance() -> CustomerSupportRAG:
    global _rag_instance
    if _rag_instance is None:
        logger.info("Initializing RAG pipeline (loading embeddings & vector store)...")
        _rag_instance = CustomerSupportRAG()
        logger.info("RAG pipeline ready.")
    return _rag_instance


def get_rag_response(user_query: str) -> str:
    return _get_instance().get_response(user_query).answer


def get_rag_response_full(user_query: str) -> RAGResult:
    return _get_instance().get_response(user_query)