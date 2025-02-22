"""路由模块

负责管理所有API路由的注册和组织。遵循DDD架构，按业务领域划分路由模块。
"""

from fastapi import APIRouter

# api根路由
api_router = APIRouter(prefix="/api")

# 导入并注册子路由器
# 随着业务模块的增加，在这里添加新的路由器