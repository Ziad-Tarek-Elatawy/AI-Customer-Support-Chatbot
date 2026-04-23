from pydantic import BaseModel

class ChatQuery(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    status: str = "success"