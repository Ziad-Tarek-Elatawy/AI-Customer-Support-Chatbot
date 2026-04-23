from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

# 1. Path Configuration
# Ensures the backend directory is recognized as a package from any execution point
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 2. Component Imports (Schemas & AI Pipeline)
try:
    # Attempting to import the AI response function from the RAG pipeline file
    from backend.ai.rag_pipeline import get_rag_response
except (ImportError, ModuleNotFoundError):
    # Fallback function in case the AI team has not implemented their logic yet
    def get_rag_response(user_query: str) -> str:
        return f"Backend connected. AI Pipeline is currently a placeholder. Received: {user_query}"

try:
    from backend.api.schemas import ChatQuery, ChatResponse
except (ImportError, ModuleNotFoundError):
    # Local import fallback for direct execution
    try:
        from schemas import ChatQuery, ChatResponse
    except ImportError:
        raise ImportError("Critical Error: schemas.py not found in the expected directory!")

# 3. App Definition
app = FastAPI(
    title="AI Customer Support Chatbot API",
    description="The core backend API for handling customer queries using RAG technology.",
    version="1.0.0"
)

# 4. CORS Middleware Setup
# Vital for allowing the Frontend (React/Flutter) to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. API Routes
@app.get("/")
def home():
    """Health check endpoint to verify server status"""
    return {
        "status": "Online", 
        "message": "AI Customer Support API is running successfully",
        "project": "AI Customer Support Chatbot"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(query: ChatQuery):
    """
    Main Chat Endpoint:
    Receives user query and passes it to the RAG Pipeline for processing.
    """
    try:
        # Calling the function from rag_pipeline.py
        # Once Mohamed and Mashhour fill the logic, this will work automatically
        answer = get_rag_response(query.message)
        
        return ChatResponse(
            answer=answer,
            confidence=0.95, # Placeholder confidence score
            status="success"
        )
    except Exception as e:
        # Standard error handling for internal server issues
        raise HTTPException(
            status_code=500, 
            detail=f"Internal Server Error: {str(e)}"
        )

# 6. Server Execution
if __name__ == "__main__":
    # Running on port 8001 to avoid common Mac port conflicts
    uvicorn.run("backend.api.main:app", host="127.0.0.1", port=8001, reload=True)