from sqlalchemy import Integer, String, DateTime, ForeignKey,Enum,Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="创建时间")
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(),onupdate=datetime.now(), comment="更新时间")


class User(Base):
    __tablename__ = 'users'

    #创建索引根据username、phone查询更快
    __table_args__ = (
        Index("username_UNIQUE", "username"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True,comment ="用户id")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False,comment ="用户名")
    password: Mapped[str] = mapped_column(String(50), nullable=False,comment= "用户密码")
    nickname: Mapped[str] = mapped_column(String(50),default="user" ,comment= "用户名称")


class UserToken(Base):
    __tablename__ = 'user_token'

    __table_args__ = (
        Index("fk_user_token_user_idx", "user_id"),
        Index("token_UNIQUE", "token"),

    )

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="令牌ID")
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False,comment="用户ID")
    token: Mapped[str] = mapped_column(String(50), unique=True, nullable=False,comment="令牌值")
    expires_at: Mapped[int] = mapped_column(DateTime,nullable=False,comment="过期时间")
    created_at : Mapped[datetime] = mapped_column(DateTime,default=datetime.now(),comment="创建时间")















