"""
数据库配置和连接管理
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# 创建异步数据库引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 自动检测断开的连接
    pool_recycle=3600,   # 连接回收秒数
    echo=False, # 是否打印SQL语句
)

# 创建异步会话工厂
SessionLocal = async_sessionmaker(
    engine,                 # 绑定引擎
    class_=AsyncSession,    # 使用异步会话
    expire_on_commit=False, # 提交后不过期
    autocommit=False,       # 自动提交
    autoflush=False,        # 自动刷新
)

async def get_db():
    """
    获取数据库会话
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
