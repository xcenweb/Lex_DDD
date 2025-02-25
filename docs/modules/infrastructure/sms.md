# 短信模块

## 模块介绍

短信模块(`sms.py`)是基础设施层的通信组件，负责处理系统中的短信发送功能，支持验证码、通知消息等场景，并提供异步发送和状态追踪能力。

## 功能特性

- 异步短信发送
- 验证码生成和验证
- 模板消息支持
- 批量发送能力
- 发送状态追踪

## 配置说明

短信服务配置项在`.env`文件中定义：

```env
# 短信服务配置
SMS_PROVIDER=aliyun
SMS_ACCESS_KEY_ID=your-access-key-id
SMS_ACCESS_KEY_SECRET=your-access-key-secret
SMS_SIGN_NAME=your-sign-name
SMS_TEMPLATE_CODE=SMS_1234567
```

## 使用示例

### 发送验证码

```python
from infrastructure.sms import SMSService

async def send_verification_code(phone: str):
    sms_service = SMSService()
    code = await sms_service.generate_verification_code()
    await sms_service.send_verification_code(
        phone=phone,
        code=code,
        template_id="VERIFY_CODE"
    )
    return code
```

### 发送通知消息

```python
from infrastructure.sms import SMSService

async def send_order_notification(phone: str, order_id: str):
    sms_service = SMSService()
    await sms_service.send_template_message(
        phone=phone,
        template_id="ORDER_CREATED",
        template_params={
            "order_id": order_id
        }
    )
```

## AI提示词使用技巧

### 1. 创建短信模板

提示词模板：
```
请帮我创建以下短信模板：
1. 模板名称：[名称]
2. 使用场景：[场景描述]
3. 变量列表：[需要的变量]
4. 内容要求：[内容规范]
5. 是否需要多语言支持
```

示例：
```
请帮我创建以下短信模板：
1. 模板名称：订单发货通知
2. 使用场景：订单已发货时通知用户
3. 变量列表：订单号、快递公司、快递单号
4. 内容要求：简洁明了，包含物流查询链接
5. 需要中英文支持
```

### 2. 短信发送配置

提示词模板：
```
请帮我配置短信发送参数：
1. 发送场景：[场景名称]
2. 重试策略：[重试规则]
3. 限流设置：[限流规则]
4. 黑名单处理：[处理方式]
5. 特殊通道：[通道选择]
```

### 3. 验证码策略

提示词模板：
```
请帮我设置验证码策略：
1. 验证码长度：[位数]
2. 有效期：[时长]
3. 重试间隔：[间隔时间]
4. 最大尝试次数：[次数]
5. 防刷策略：[策略描述]
```

## 最佳实践

1. 使用异步发送
2. 实现重试机制
3. 添加发送限流
4. 记录发送日志
5. 监控发送状态

## 常见问题

1. **发送失败**
   - 原因：运营商网关问题
   - 解决：启用备用通道

2. **验证码未收到**
   - 原因：手机号码格式错误
   - 解决：加强号码验证

3. **发送延迟**
   - 原因：网络拥堵
   - 解决：使用多通道策略

## 注意事项

1. 保护用户隐私
2. 遵守发送频率限制
3. 实现防刷机制
4. 监控发送成本
5. 处理退订请求