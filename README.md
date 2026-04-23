# Customer Support RAG-Powered Intelligent Chatbot

## Project Overview
Build a production-ready support automation system using **Retrieval-Augmented Generation (RAG)** and vector search. It is designed to serve real customer queries and integrate directly with business backend systems.

## Project Structure
To ensure clean collaboration, the project is divided into distinct directories:

```text
.
├── backend/
│   ├── ai/          # RAG pipeline, LLM integration, Vector DB scripts
│   ├── api/         # FastAPI application and REST endpoints
│   └── tests/       # Unit and integration tests
├── data/
│   ├── raw/         # Unprocessed historical support tickets and FAQs
│   └── processed/   # Cleaned text data ready for embeddings
├── docs/            # Project documentation 
├── frontend/        # Chatbot web widget & UI (if required)
├── mlops/           # Deployment scripts, Azure config, and MLflow setup
└── notebooks/       # Jupyter notebooks for EDA and model evaluation
```

## Project Milestones

### Milestone 1: Data Collection & Preprocessing
*   **Objectives:** Aggregate support ticket logs, FAQs, documentation, and knowledge base.
*   **Deliverables:** Processed Text Corpus, Preprocessing Pipeline Doc, Support Data EDA Report.

### Milestone 2: Model Development & Evaluation
*   **Objectives:** Train and evaluate the RAG retrieval + generation pipeline.
*   **Deliverables:** Trained RAG Pipeline, Model Evaluation Report (using metrics like BLEU, ROUGE, relevance).

### Milestone 3: Advanced Techniques & Azure Deployment
*   **Objectives:** Deploy intelligent chatbot as part of production support.
*   **Deliverables:** Deployed Chatbot Service via Azure (App Service / Machine Learning), Integration Docs, Secure endpoints via Azure AD or API keys.

### Milestone 4: MLOps & Monitoring
*   **Objectives:** Track performance and automate retraining using MLflow.
*   **Deliverables:** Monitoring Dashboard (latency, accuracy, SAT scores), Retraining Pipeline.

### Milestone 5: Final Documentation & Presentation
*   **Objectives:** Finalize project deliverables for evaluation.
*   **Deliverables:** Final Report, Demo Presentation, Business KPI Impact Analysis.

## Technology Stack
*   **AI Frameworks:** Hugging Face, LangChain, OpenAI/OpenRouter (LLMs).
*   **MLOps & Eval:** MLflow, Python NLP libraries (for BLEU/ROUGE).
*   **Database & Search:** Azure Cognitive Search (or ChromaDB locally).
*   **Backend & Cloud:** FastAPI (Python), Microsoft Azure.
