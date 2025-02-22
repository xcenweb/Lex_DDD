"""
应用生命周期
"""

from fastapi import FastAPI
from sqlalchemy import text
from contextlib import asynccontextmanager

from src.infrastructure.database import engine
from src.infrastructure.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理器

    负责管理应用启动和关闭时的资源初始化和清理工作
    """

    if settings.DEBUG:
        print("\033[93m请注意！！！当前为调试模式！！！请勿在生产环境中运行！！！\033[0m")
    else:
        print("\033[92m调试模式已关闭！！！\033[0m")

    try:
        # 确保数据库引擎已经准备就绪
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("数据库连接测试成功")

        yield
    finally:
        # 关闭时的清理操作
        print("清理...")
        await engine.dispose()
        print("数据库连接池已关闭")