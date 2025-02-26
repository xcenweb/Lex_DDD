# 路由组件 (Routers)

## 概述

`routers/` 目录采用模块化设计，包含所有API路由定义。系统实现了自动路由注册机制，会自动扫描并注册该目录下的所有路由模块。

## 路由架构

```python
src/interfaces/routers/
├── __init__.py      # 路由注册器
├── base.py          # 基础路由
└── [module].py      # 功能模块路由
```

## 自动注册机制

系统会自动扫描`routers/`目录下的所有Python文件，并注册其中定义的路由对象：

```python
# routers/__init__.py
from fastapi import APIRouter
from pathlib import Path
import importlib

router = APIRouter()

def register_routers():
    current_dir = Path(__file__).parent
    for route_file in current_dir.glob("*.py"):
        if route_file.stem != "__init__":
            module = importlib.import_module(f"{__package__}.{route_file.stem}")
            if hasattr(module, "router"):
                router.include_router(module.router)

register_routers()
```

## 创建新路由

```
请帮我创建[模块名称]的路由模块：
1. 在routers目录下创建新的路由文件
2. 定义路由前缀和标签
3. 实现基础的CRUD接口
4. 添加接口文档
5. 实现错误处理
```

示例结果：
```python
"""用户路由模块

包含用户相关的API接口
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..responses import BaseResponse
from ...application.services import UserService
from ...domain.entities import UserCreate, UserUpdate

# 创建路由对象
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=BaseResponse)
async def create_user(user: UserCreate, service: UserService = Depends()):
    """创建新用户
    
    Args:
        user: 用户创建数据
        service: 用户服务实例
    
    Returns:
        BaseResponse: 统一响应格式
    """
    try:
        result = await service.create_user(user)
        return BaseResponse(code=200, message="创建成功", data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## 最佳实践

1. 路由组织
   - 按功能模块分组
   - 使用版本控制
   - 遵循RESTful规范

2. 错误处理
   - 统一异常处理器
   - 友好的错误提示
   - 日志记录

3. 文档生成
   - 添加OpenAPI注释
   - 包含请求示例
   - 说明响应格式