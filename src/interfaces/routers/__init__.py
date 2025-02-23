"""路由模块

负责管理所有API路由的注册和组织。遵循DDD架构，按业务领域划分路由模块。
"""

from fastapi import APIRouter

# api根路由
api_router = APIRouter(prefix="/api")

# 导入并注册子路由器
# 随着业务模块的增加，在这里添加新的路由器
from .user import router as user_router
from .test import router as test_router
api_router.include_router(user_router)
api_router.include_router(test_router)