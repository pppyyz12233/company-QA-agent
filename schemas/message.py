from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str  #用户的问题
    conversation_id: Optional[int] = None


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    sources: Optional[List[Dict[str, Any]]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    question: str  #用户的问题
    conversation_id: Optional[int] = None  #会话ID


class ChatResponse(BaseModel):
    answer: str  #AI的回答
    sources: List[str]  #引用的来源
    conversation_id: int  #会话ID
    message_id: int  #消息ID