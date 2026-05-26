import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User, UserToken
from schemas.user import UserCreate, UserUpdateRequest, UserChangePasswordRequest
from utils.auth import hash_password, verify_password


#创建用户
async def creat_user(
        db:AsyncSession,
        user_data:UserCreate
):
    stmt = select(User).where(User.username == user_data.username)

    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        return None

    hashed_password = hash_password(user_data.password)
    sttm = User(username=user_data.username,password=hashed_password)

    db.add(sttm)
    await db.commit()
    await db.refresh(sttm)
    return sttm



#生成token
async def make_token(
        db:AsyncSession,
        user_id:int
):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id,token=token,expires_at=expires_at)

        db.add(user_token)
        await db.commit()
        await db.refresh(user_token)

    return user_token


#根据用户名获取用户信息
async def get_user(
        db:AsyncSession,
        username:str
):
    sttm = select(User).where(User.username == username)
    result = await db.execute(sttm)
    return result.scalar_one_or_none()


#用户登录
async def user_login(
        db:AsyncSession,
        username:str,
        password:str
):
    sttm = await get_user(db,username)

    if not sttm:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    valid = verify_password(password, sttm.password)

    if not valid:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = await make_token(db, sttm.id)
    return sttm, token


#修改用户信息
async def revise_user_information(
        db:AsyncSession,
        user:User,
        updata: UserUpdateRequest
):
    if not user:
        HTTPException(status_code=404)
    user.nickname = updata.nickname
    user.phone = updata.phone
    user.avatar = updata.avatar
    user.bio = updata.bio
    user.gender = updata.gender

    await db.commit()
    await db.refresh(user)

    return user


#修改密码
async def revise_user_password(
        db:AsyncSession,
        user:User,
        password_data: UserChangePasswordRequest
):
    if not verify_password(password_data.old_password, user.password):
        return False

    new_hashed_password = hash_password(password_data.new_password)
    user.password = new_hashed_password
    await db.commit()
    await db.refresh(user)

    return True


#根据token获取用户信息
async def get_user_by_token(
        db: AsyncSession,
        token: str
):
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    user_token = result.scalar_one_or_none()

    if not user_token:
        return None

    if user_token.expires_at < datetime.now():
        return None

    stmt = select(User).where(User.id == user_token.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    return user