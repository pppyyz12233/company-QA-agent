from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/school_app?charset=utf8"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # sql日志(可选)
    pool_size=10,  # 设置连接池保持持久连接数
    max_overflow=20  # 设置地址池允许创建额外的连接数

)


# 创建异步会话工厂
Async = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False  # 会话对象不过期，不会重新查询数据库
)


# 获取数据库会话
async def get_db():
    async with Async() as session:
        try:
            yield session  # 返回数据库会话给路由处理
            await session.commit()  # 提交事务
        except Exception:
            await session.rollback()  # 有异常回滚
            raise
        finally:
            await session.close()  # 关闭会话