"""
应用生命周期
"""

from fastapi import FastAPI
from sqlalchemy import text
from contextlib import asynccontextmanager

from app.core.db import engine
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理器

    负责管理应用启动和关闭时的资源初始化和清理工作
    """

    if settings.DEBUG:
        print("\033[93m请注意！！！当前为调试模式！！！切勿在生产环境中运行！！！\033[0m")
    else:
        print("\033[92m调试模式已关闭！！！\033[0m")

    try:
        # 确保数据库引擎已经准备就绪
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("\033[92m-数据库连接测试成功\033[0m")
        yield
        print("\033[92m-应用已关闭\033[0m")
    except Exception as e:
        print("\033[91m-数据库连接测试失败\033[0m", e)
    finally:
        # 关闭时的清理操作
        await engine.dispose() # 关闭数据库连接池