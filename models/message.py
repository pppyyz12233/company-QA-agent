from sqlalchemy import Integer, DateTime, Enum,  JSON, func, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
class Message(Base):

    __tablename__ = "messages"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    conversation_id:Mapped[int] = mapped_column(Integer, nullable=False)
    role:Mapped[str] = mapped_column(Enum("user", "assistant"), nullable=False)
    content:Mapped[str] = mapped_column(Text, nullable=False)
    sources:Mapped[dict] = mapped_column(JSON, nullable=True)
