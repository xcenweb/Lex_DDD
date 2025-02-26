# 响应组件 (Responses)

## 概述

`responses.py` 负责定义统一的响应格式和数据模型，确保系统返回一致的数据结构。

## 基础响应模型

```python
# 示例响应模型
from pydantic import BaseModel

class BaseResponse(BaseModel):
    code: int
    message: str
    data: dict | None
```

## 响应模型开发

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

2. 参数验证
   - 使用Pydantic模型
   - 添加详细的验证规则
   - 提供清晰的错误提示