from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.conversation import Conversation


#根据用户id获取用户的所有会话列表
async def get_conversations_by_user(
        db: AsyncSession,
        user_id: int
):
    stmt = select(Conversation).where(Conversation.user_id == user_id).order_by(desc(Conversation.updated_at))

    result = await db.execute(stmt)
    conversations = result.scalars().all()

    return conversations if conversations is not None else []

#根据user_id获取全部列表
async def get_conversation_by_id(
        db:AsyncSession,
        conversation_id: int,
        user_id:int
):
    sttm = select(Conversation).where(Conversation.id == conversation_id,Conversation.user_id == user_id)

    response = await db.execute(sttm)
    return response.scalar_one_or_none()

#创建列表
async def create_conversation(
        db:AsyncSession,
        user_id: int,
        title: str
):
    sttm = Conversation(user_id = user_id, title = title)

    db.add(sttm)
    await db.commit()
    await db.refresh(sttm)
    return sttm

#修改列表标题
async def update_conversation_title(
        db:AsyncSession,
        conversation_id: int,
        user_id,
        title: str
):
    sttm = update(Conversation).where(Conversation.id == conversation_id,Conversation.user_id ==user_id).values(title=title, updated_at=datetime.now())

    result =await db.execute(sttm)
    await db.commit()
    if result.rowcount == 0:#用rowcount(有被修改更新的返回数字)查看result里有没有被修改
        raise HTTPException(status_code=404, detail='对话列表不存在')

    return await get_conversation_by_id(db, conversation_id, user_id)


#删除列表
async def delete_conversation(
        db:AsyncSession,
        conversation_id: int,
        user_id: int,
):
    conversation = await get_conversation_by_id(db, conversation_id,user_id)

    await db.delete(conversation)
    await db.commit()
    return conversation