# 邮件模块

## 模块介绍

邮件模块(`email.py`)是基础设施层的通信组件，负责处理系统中的邮件发送功能，支持HTML模板、附件处理和异步发送等特性。

## 功能特性

- 异步邮件发送
- HTML邮件模板支持
- 附件处理
- 批量发送
- 发送状态追踪

## 配置说明

邮件服务配置项在`.env`文件中定义：

```env
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-password
SMTP_TLS=true
MAIL_FROM=noreply@example.com
```

## 使用示例

### 发送简单邮件

```python
from infrastructure.email import EmailService

async def send_welcome_email(user_email: str, username: str):
    email_service = EmailService()
    await email_service.send_email(
        to_email=user_email,
        subject="欢迎加入",
        content=f"你好 {username}，欢迎使用我们的服务！"
    )
```

### 使用HTML模板

```python
from infrastructure.email import EmailTemplate

async def send_order_confirmation(order_id: str, user_email: str):
    template = EmailTemplate("order_confirmation")
    html_content = template.render(
        order_id=order_id,
        date=datetime.now()
    )
    await email_service.send_html_email(
        to_email=user_email,
        subject="订单确认",
        html_content=html_content
    )
```

## AI提示词使用技巧

### 1. 创建邮件模板

提示词模板：
```
请帮我创建以下邮件模板：
1. 模板名称：[名称]
2. 使用场景：[场景描述]
3. 变量列表：[需要的变量]
4. 样式要求：[样式说明]
5. 是否需要多语言支持
```

示例：
```
请帮我创建以下邮件模板：
1. 模板名称：密码重置
2. 使用场景：用户申请重置密码时发送验证邮件
3. 变量列表：用户名、重置链接、过期时间
4. 样式要求：简洁大方，突出重置链接
5. 需要中英文支持
```

### 2. 邮件发送配置

提示词模板：
```
请帮我配置邮件发送参数：
1. 发送场景：[场景名称]
2. 重试策略：[重试规则]
3. 优先级设置：[优先级]
4. 追踪要求：[是否需要追踪]
5. 特殊处理：[其他要求]
```

### 3. 批量发送优化

提示词模板：
```
请帮我优化批量邮件发送：
1. 发送数量：[邮件数量]
2. 性能要求：[性能指标]
3. 错误处理：[处理方式]
4. 监控需求：[监控指标]
```

## 最佳实践

1. 使用异步发送
2. 实现重试机制
3. 记录发送日志
4. 设置发送限流
5. 监控发送状态

## 常见问题

1. **发送失败**
   - 原因：SMTP配置错误
   - 解决：检查配置参数

2. **邮件被标为垃圾邮件**
   - 原因：内容或发送策略问题
   - 解决：优化内容和发送频率

3. **模板渲染错误**
   - 原因：变量未定义
   - 解决：检查模板变量

## 注意事项

1. 保护敏感信息
2. 遵守发送频率限制
3. 实现退订机制
4. 定期清理发送记录
5. 监控垃圾邮件投诉