"""路由模块

负责管理所有API路由的注册和组织。遵循DDD架构，按业务领域划分路由模块。
"""

from fastapi import APIRouter

# 创建根路由器
api_router = APIRouter(prefix="/api/v1")

# 导入并注册子路由器
# TODO: 随着业务模块的增加，在这里添加新的路由器
# from .user import router as user_router
# from .prompt import router as prompt_router
# api_router.include_router(user_router)
# api_router.include_router(prompt_router)