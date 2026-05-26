from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from crud import user
from stock.db import get_db
from chat_service.chat import process_question, get_conversation_history



router = APIRouter(prefix="/api/chat", tags=["智能问答"])
security = HTTPBearer()


#智能问答接口
@router.post("")
async def chat(
    request: dict,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db)
):
    try:
        question = request.get("question")#前端{"question": "年假几天？", "conversation_id": 1}
        conversation_id = request.get("conversation_id")

        if not question:
            raise HTTPException(status_code=400, detail="问题不能为空")

        #验证用户身份
        token = credentials.credentials
        current_user = await user.get_user_by_token(db, token)

        if not current_user:
            raise HTTPException(status_code=401, detail="无效的令牌")


        #调用业务逻辑处理问题
        result = await process_question(
            db=db,
            user_id=current_user.id,
            question=question,
            conversation_id=conversation_id
        )

        #返回响应
        return {
            "code": 200,
            "message": "问答成功",
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"处理问题异常: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"处理问题失败：{str(e)}")


#获取聊天历史
@router.get("/history/{conversation_id}")
async def get_history(
    conversation_id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db)
):
    try:
        token = credentials.credentials
        current_user = await user.get_user_by_token(db, token)

        if not current_user:
            raise HTTPException(status_code=401, detail="无效的令牌")

        result = await get_conversation_history(
            db=db,
            user_id=current_user.id,
            conversation_id=conversation_id
        )

        return {
            "code": 200,
            "message": "获取聊天历史成功",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取历史异常: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取历史失败：{str(e)}")