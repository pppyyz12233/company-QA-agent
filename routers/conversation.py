from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession


from crud import conversation, user
from schemas.conversation import ConversationCreate, ConversationUpdate
from stock.db import get_db

router = APIRouter(prefix="/api/conversations", tags=["对话列表"])
security = HTTPBearer()


#获取用户列表
@router.get("/all_conversations")
async def get_all_conversations(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    current_user = await user.get_user_by_token(db, token)

    if not current_user:
        raise HTTPException(status_code=401, detail="无效的令牌")

    conversations = await conversation.get_conversations_by_user(db, current_user.id)

    return {
        "code": 200,
        "message": "获取会话列表成功",
        "data": {
            "conversations": [
                {
                    "id": conv.id,
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                }
                for conv in conversations
            ],
            "total": len(conversations)
        }
    }


#创建列表
@router.post("/creat_conversation")
async def create_conversation(
        data: ConversationCreate,
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    current_user = await user.get_user_by_token(db, token)

    if not current_user:
        raise HTTPException(status_code=401, detail="无效的令牌")

    new_conversation = await conversation.create_conversation(db,current_user.id,data.title)

    return {
        "code": 200,
        "message": "创建会话成功",
        "data": {
            "id": new_conversation.id,
            "user_id": new_conversation.user_id,
            "title": new_conversation.title,
            "created_at": new_conversation.created_at.isoformat(),
            "updated_at": new_conversation.updated_at.isoformat()
        }
    }



#重命名列表
@router.put("/rename_conversation")
async def rename_conversation(
        conversation_id: int,
        data:ConversationUpdate,
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    current_user = await user.get_user_by_token(db, token)

    if not current_user:
        raise HTTPException(status_code=401, detail="无效的令牌")

    response = await conversation.update_conversation_title(db, conversation_id, current_user.id, data.title)

    return{
        "code": 200,
        "message": "重命名成功",
        "data": {
            "id": response.id,
            "title": response.title
        }
    }


#删除列表
@router.delete("/{conversation_id}")
async def delete_conversation(
        conversation_id :int,
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    current_user = await user.get_user_by_token(db, token)

    if not current_user:
        raise HTTPException(status_code=401, detail="无效的令牌")


    await conversation.delete_conversation(db, conversation_id, current_user.id)

    return {
        "code": 200,
        "message": "删除会话成功",
        "data": None
    }