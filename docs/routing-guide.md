# 路由配置指南

## 概述

本文档提供了在LexDDD框架下进行路由配置的最佳实践和指导原则，帮助开发者构建符合DDD架构的API接口。

## 路由组织原则

1. **分层结构**
   - 路由定义位于接口层（interfaces）
   - 通过依赖注入获取应用服务
   - 保持路由处理器的简洁性

2. **模块化组织**
   - 按业务领域划分路由模块
   - 使用FastAPI的APIRouter进行模块化管理
   - 统一的路由注册机制

## 最佳实践

### 1. 路由定义

```python
from fastapi import APIRouter, Depends
from src.application.user import UserService
from src.interfaces.responses import Response

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
async def register_user(
    request: UserRegisterRequest,
    user_service: UserService = Depends(get_user_service)
) -> Response:
    result = await user_service.register(request)
    return Response.success(result)
```

### 2. 依赖注入

```python
from fastapi import Depends
from src.infrastructure.database import get_db

def get_user_service(db = Depends(get_db)) -> UserService:
    return UserService(db)
```

### 3. 错误处理

```python
from fastapi import HTTPException
from src.infrastructure.exceptions import BusinessError

@router.exception_handler(BusinessError)
async def business_exception_handler(request, exc):
    return Response.error(str(exc))
```

## 路由配置规范

1. **URL命名规范**
   - 使用小写字母和连字符
   - RESTful风格的资源命名
   - 版本号放在URL前缀

2. **HTTP方法使用**
   - GET：查询操作
   - POST：创建操作
   - PUT：全量更新
   - PATCH：部分更新
   - DELETE：删除操作

3. **响应格式**
   - 统一使用Response封装
   - 包含状态码和消息
   - 规范的错误码体系

## 常见问题

1. **如何处理跨域请求？**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_methods=["*"],
       allow_headers=["*"]
   )
   ```

2. **如何实现路由中间件？**
   ```python
   from fastapi import Request
   
   @router.middleware("http")
   async def add_process_time_header(request: Request, call_next):
       start_time = time.time()
       response = await call_next(request)
       process_time = time.time() - start_time
       response.headers["X-Process-Time"] = str(process_time)
       return response
   ```

3. **如何进行请求验证？**
   ```python
   from pydantic import BaseModel, validator
   
   class UserRequest(BaseModel):
       username: str
       email: str
       
       @validator("email")
       def validate_email(cls, v):
           if "@" not in v:
               raise ValueError("Invalid email format")
           return v
   ```

## 安全性考虑

1. **认证与授权**
   - 使用JWT进行身份认证
   - 基于角色的访问控制
   - 请求签名验证

2. **数据验证**
   - 输入数据清洗
   - 参数类型检查
   - 业务规则验证

3. **安全防护**
   - CORS配置
   - Rate Limiting
   - SQL注入防护

## 测试策略

1. **单元测试**
   ```python
   from fastapi.testclient import TestClient
   
   def test_register_user():
       client = TestClient(app)
       response = client.post(
           "/users/register",
           json={"username": "test", "email": "test@example.com"}
       )
       assert response.status_code == 200
       assert response.json()["code"] == 0
   ```

2. **集成测试**
   - 测试完整的请求流程
   - 验证中间件功能
   - 检查数据库交互

## 性能优化

1. **异步处理**
   - 使用异步路由处理器
   - 异步数据库操作
   - 并发请求处理

2. **缓存策略**
   - 响应缓存
   - 数据缓存
   - 缓存失效机制

## 文档生成

1. **OpenAPI规范**
   ```python
   from fastapi import FastAPI
   
   app = FastAPI(
       title="LexDDD API",
       description="LexDDD项目API文档",
       version="1.0.0"
   )
   ```

2. **接口注释**
   ```python
   @router.post("/register", response_model=Response)
   async def register_user(request: UserRegisterRequest):
       """用户注册接口
       
       Args:
           request: 注册请求参数
           
       Returns:
           Response: 统一响应格式
       """
   ```

## 总结

良好的路由配置是构建高质量API的基础，需要注意：
1. 遵循DDD架构原则
2. 保持代码的清晰和模块化
3. 注重安全性和性能优化
4. 完善的测试和文档