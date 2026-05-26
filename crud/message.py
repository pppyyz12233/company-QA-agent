from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.conversation import get_conversation_by_id
from models.conversation import Conversation
from models.message import Message


#将用户和AI的对话消息保存到数据库
async def save_message(
        db: AsyncSession,
        conversation_id: int,
        role: str, content: str,
        sources: list = None
):
    message = Message(conversation_id=conversation_id,role=role,content=content,sources=sources or [])

    db.add(message)
    await db.commit()
    await db.refresh(message)

    stmt = select(Conversation).where(Conversation.id == conversation_id)
    result = await db.execute(stmt)
    conversation = result.scalar_one_or_none()

    if conversation:
        conversation.updated_at = datetime.now()
        await db.commit()

    return message


#获取会话中的所有消息
async def get_messages_by_conversation(
        db: AsyncSession,
        conversation_id: int,
        user_id: int = None
):
    if user_id:
        conversation = await get_conversation_by_id(db, conversation_id, user_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="会话不存在")

    stmt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    result = await db.execute(stmt)

    return result.scalars().all()

