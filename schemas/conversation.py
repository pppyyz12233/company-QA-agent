from typing import Optional
from pydantic import BaseModel


class ConversationCreate(BaseModel):
    title: Optional[str] = "新对话"

class ConversationUpdate(BaseModel):
    title: str