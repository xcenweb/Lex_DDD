"""基础路由模块

包含系统基础路由，如根路由等
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    """
    根路径
    """
    return {"message": "欢迎使用LexTrade API服务"}