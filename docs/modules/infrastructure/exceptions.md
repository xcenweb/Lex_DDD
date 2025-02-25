# 异常处理模块

## 模块介绍

异常处理模块(`exceptions.py`)是基础设施层的错误处理组件，提供统一的异常定义、处理和日志记录机制，确保系统能够优雅地处理各类错误情况。

## 功能特性

- 统一的异常类型体系
- 自定义业务异常支持
- 异常链追踪
- 错误码管理
- 多语言错误消息

## 异常类型说明

```python
# 基础异常类
class BaseException(Exception):
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code

# 业务异常
class BusinessException(BaseException):
    """业务逻辑异常"""
    pass

# 验证异常
class ValidationException(BaseException):
    """数据验证异常"""
    pass

# 权限异常
class PermissionException(BaseException):
    """权限验证异常"""
    pass
```

## 使用示例

### 基本异常处理

```python
from infrastructure.exceptions import BusinessException

def process_order(order_data: dict):
    try:
        # 业务处理逻辑
        if not order_data.get('user_id'):
            raise BusinessException('用户ID不能为空', code='ORDER001')
    except BusinessException as e:
        logger.error(f'订单处理失败：{e.message}')
        raise
```

### 全局异常处理

```python
from fastapi import FastAPI
from infrastructure.exceptions import exception_handler

app = FastAPI()

@app.exception_handler(BusinessException)
async def business_exception_handler(request, exc):
    return exception_handler.handle_business_exception(exc)
```

## AI提示词使用技巧

### 1. 创建自定义异常

提示词模板：
```
请帮我创建以下自定义异常：
1. 异常名称：[名称]
2. 异常类型：[类型]
3. 错误码：[错误码规则]
4. 错误消息：[消息模板]
5. 是否需要国际化
```

示例：
```
请帮我创建以下自定义异常：
1. 异常名称：订单状态异常
2. 异常类型：业务异常
3. 错误码：ORDER_STATUS_ERROR
4. 错误消息：订单{order_id}状态{current_status}不允许{operation}
5. 需要中英文支持
```

### 2. 异常处理策略

提示词模板：
```
请帮我设计以下异常处理策略：
1. 异常场景：[场景描述]
2. 处理方式：[处理方法]
3. 日志级别：[日志等级]
4. 重试策略：[是否重试]
5. 通知方式：[通知渠道]
```

### 3. 错误码规范

提示词模板：
```
请帮我定义以下错误码规范：
1. 业务模块：[模块名]
2. 错误类型：[类型列表]
3. 码值范围：[取值范围]
4. 格式要求：[格式规范]
5. 示例说明：[示例代码]
```

## 最佳实践

1. 使用自定义异常
2. 实现统一处理
3. 详细记录日志
4. 合理设置重试
5. 规范错误码

## 常见问题

1. **异常信息不完整**
   - 原因：异常捕获不当
   - 解决：完善异常信息

2. **异常处理性能问题**
   - 原因：处理逻辑复杂
   - 解决：优化处理流程

3. **重复异常处理**
   - 原因：多层异常捕获
   - 解决：统一处理层级

## 注意事项

1. 避免吞没异常
2. 保持异常粒度合适
3. 规范错误码管理
4. 完善错误提示
5. 记录详细日志