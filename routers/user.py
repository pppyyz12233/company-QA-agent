from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from crud import user
from crud.user import revise_user_password
from schemas.user import UserCreate, UserUpdateRequest, UserChangePasswordRequest
from stock.db import get_db


router = APIRouter(prefix="/api/user", tags=["用户"])
security = HTTPBearer()

#获取当前用户信息
@router.get("/info")
async def me(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    current_user = await user.get_user_by_token(db, token)

    if not current_user:
        raise HTTPException(status_code=401, detail="无效的令牌")

    return {
        "code": 200,
        "message": "获取用户信息成功",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "nickname": current_user.nickname,
        }
    }

#用户注册
@router.post("/register")
async def get_user(
        user_data:UserCreate,
        db:AsyncSession = Depends(get_db)
):
    new_user = await user.creat_user(db,user_data)

    if new_user is None:
        raise HTTPException(status_code=400,detail=f"用户名 '{user_data.username}' 已被占用，请选择其他用户名。")

    token_obj = await user.make_token(db, new_user.id)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": token_obj.token,
            "user_id": new_user.id,
            "username": new_user.username,
            "nickname": new_user.nickname
        }
    }


#用户登录
@router.post("/login")
async def user_login(
        user_data:UserCreate,
        db:AsyncSession = Depends(get_db)
):
    user_login,token1 = await user.user_login(db,user_data.username,user_data.password)

    if not user_login:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": token1.token,
            "user_id": user_login.id,
            "username": user_login.username,
            "nickname": user_login.nickname,
        }
    }

#修改用户信息
@router.put("/revise")
async def revise_user(
        user_data:UserUpdateRequest,
        credentials: HTTPAuthorizationCredentials = Security(security),
        db:AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    current_user = await user.get_user_by_token(db, token)

    if not current_user:
        raise HTTPException(status_code=401, detail="无效的令牌")

    response = await user.revise_user_information(db,current_user,user_data)
    return {
        "code": 200,
        "message": "更新成功",
        "data": {
                    "id": response.id,
                    "username": response.username,
                    "nickname": response.nickname,
                    "phone": response.phone,
                    "avatar": response.avatar,
                    "gender": response.gender,
                    "bio": response.bio,
                }
    }


#修改用户密码
@router.put("/revise_password")
async def revise_password(
        userdata: UserChangePasswordRequest,
        credentials: HTTPAuthorizationCredentials = Security(security),
        db:AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    current_user = await user.get_user_by_token(db, token)

    if not current_user:
        raise HTTPException(status_code=401, detail="无效的令牌")

    success = await revise_user_password(db, current_user, userdata)

    if not success:
        raise HTTPException(status_code=400, detail="旧密码错误")
    return {"message": "用户名密码修改成功"}
