
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    password: str = Field(..., max_length=50)

#更新用户信息
class UserUpdateRequest(BaseModel):
    nickname: str =None

#更新密码
class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="OldPassword",description="旧密码")
    new_password: str = Field(..., min_length=1,alias="NewPassword",description="新密码")

class Config:
        populate_by_name = True