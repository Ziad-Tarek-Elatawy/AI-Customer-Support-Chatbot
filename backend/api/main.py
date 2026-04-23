from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Handling imports
try:
    from backend.api.schemas import ChatQuery, ChatResponse
except ImportError:
    try:
        from schemas import ChatQuery, ChatResponse
    except ImportError:
        raise ImportError("Could not find schemas.py. Please ensure it exists in the same directory.")

# 1. Define the App
app = FastAPI(
    title="AI Customer Support Chatbot API",
    description="The core backend API for handling customer queries using RAG technology.",
    version="1.0.0"
)

# 2. Add CORS Middleware (Right here after app definition)
# This allows your frontend (UI) to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# 3. Routes
@app.get("/")
def home():
    """Health check endpoint"""
    return {
        "status": "Online", 
        "message": "AI Customer Support API is running successfully",
        "project": "AI Customer Support Chatbot"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(query: ChatQuery):
    """Main chat endpoint"""
    try:
        mock_answer = (
            f"Hello! We have received your message: '{query.message}'. "
            f"The system is currently being integrated with our AI engine."
        )
        
        return ChatResponse(
            answer=mock_answer,
            confidence=0.99,
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Internal Server Error: {str(e)}"
        )

# 4. Run the Server
if __name__ == "__main__":
    uvicorn.run("backend.api.main:app", host="127.0.0.1", port=8001, reload=True)