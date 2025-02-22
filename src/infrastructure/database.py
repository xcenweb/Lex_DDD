"""数据库配置和连接管理"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# 数据库连接URL（使用异步MySQL驱动）
DATABASE_URL = "mysql+aiomysql://root:root@127.0.0.1:3306/lextrade"

# 创建异步数据库引擎
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 自动检测断开的连接
    pool_recycle=3600,   # 连接回收时间（1小时）
    echo=False           # 是否打印SQL语句（生产环境建议设为False）
)

# 声明基类
class Base(DeclarativeBase):
    pass

# 创建异步会话工厂
SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# 获取异步数据库会话的依赖函数
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
