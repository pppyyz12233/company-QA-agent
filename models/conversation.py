from datetime import datetime
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(),server_default=func.now())


class Conversation(Base):

    __tablename__ = "conversations"

    id:Mapped[int] =mapped_column(Integer, primary_key=True,autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    title:Mapped[str] = mapped_column(String(100), default="新对话")
