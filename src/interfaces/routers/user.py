"""用户相关路由

处理用户注册、登录、信息管理等相关请求。
遵循DDD架构，路由处理函数通过应用层服务调用领域层业务逻辑。
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

# 创建路由器
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", summary="测试")
async def test():
    return 'ok'