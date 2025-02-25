# 接口层 (Interfaces)

## 概述

接口层是系统与外部世界交互的门户，负责处理所有进出系统的请求和响应。它主要包含以下职责：

- 处理HTTP请求和响应
- 实现API路由管理
- 请求参数验证
- 响应数据格式化
- 错误处理和异常转换

## 核心组件

### Responses

`responses.py` 负责定义统一的响应格式和数据模型：

```python
# 示例响应模型
from pydantic import BaseModel

class BaseResponse(BaseModel):
    code: int
    message: str
    data: dict | None
```

### Routers

`routers/` 目录包含所有API路由定义：

```python
# 示例路由定义
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1")

@router.get("/resource")
async def get_resource():
    return {"data": "resource"}
```

## 开发指南

### 路由开发

```
请帮我实现[功能名称]的API路由：
1. 定义路由路径和方法
2. 添加请求参数验证
3. 实现响应模型
4. 添加权限验证
5. 处理异常情况
```

示例结果：
```python
from fastapi import APIRouter, Depends, HTTPException
from ..application.services import UserService
from .responses import BaseResponse

router = APIRouter(prefix="/users")

@router.post("/")
async def create_user(user_data: UserCreate, service: UserService = Depends()):
    try:
        user = await service.create_user(user_data)
        return BaseResponse(code=200, message="success", data=user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### 响应模型开发

```
请帮我定义[功能名称]的响应模型：
1. 设计数据结构
2. 添加字段验证
3. 实现序列化方法
4. 添加示例数据
```

示例结果：
```python
from pydantic import BaseModel, Field
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    status: str = Field(default="active")
    profile: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "username": "test_user",
                "email": "test@example.com",
                "status": "active",
                "profile": {"avatar": "url"}
            }
        }
```

## 最佳实践

1. 统一响应格式
   - 使用统一的响应模型
   - 保持一致的错误码规范
   - 规范化异常处理

2. 路由组织
   - 按功能模块分组
   - 使用版本控制
   - 遵循RESTful规范

3. 参数验证
   - 使用Pydantic模型
   - 添加详细的验证规则
   - 提供清晰的错误提示

4. 文档生成
   - 添加OpenAPI注释
   - 包含请求示例
   - 说明响应格式

## 常见问题

1. 跨域处理
   - 使用CORS中间件
   - 配置允许的源和方法

2. 认证授权
   - 实现JWT认证
   - 添加权限中间件
   - 角色访问控制

3. 性能优化
   - 使用缓存
   - 实现分页
   - 控制响应大小

4. 错误处理
   - 统一异常处理器
   - 友好的错误提示
   - 日志记录