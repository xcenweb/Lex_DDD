# 环境配置指南

## 配置文件说明

LexTrade Backend使用`.env`文件进行环境配置管理。项目提供了`.env.example`作为配置模板，开发者需要基于此模板创建自己的`.env`文件。

## 配置项分类

### 基础配置

```ini
# 应用配置
APP_NAME=LexTrade
ENV=development  # development/testing/production
DEBUG=true
SECRET_KEY=your-secret-key
```

### 数据库配置

```ini
# 数据库连接配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lextrade
DB_USER=postgres
DB_PASSWORD=your-password
```

### 邮件配置

```ini
# SMTP邮件服务配置
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-password
MAIL_FROM=noreply@example.com
```

### 短信配置

```ini
# 短信服务配置
SMS_PROVIDER=aliyun  # 短信服务提供商
SMS_ACCESS_KEY=your-access-key
SMS_SECRET_KEY=your-secret-key
SMS_SIGN_NAME=您的签名
SMS_TEMPLATE_CODE=SMS_XXXXXXXX
```

## 配置最佳实践

1. **安全性**
   - 不要将`.env`文件提交到版本控制系统
   - 使用强密码和密钥
   - 定期轮换敏感配置

2. **开发流程**
   - 本地开发时复制`.env.example`为`.env`
   - 根据实际需求修改配置值
   - 新增配置项时同步更新`.env.example`

3. **配置验证**
   - 使用Pydantic进行配置验证
   - 在应用启动时验证必要配置
   - 提供合理的默认值

## AI开发建议

### 配置管理提示词

#### 添加新配置项

```
请帮我添加[功能名称]相关的环境配置：
1. 定义必要的配置项
2. 设置合理的默认值
3. 更新配置文档
4. 添加配置验证
```

#### 更新配置文档

```
请帮我更新环境配置文档：
1. 添加新增配置项说明
2. 补充配置示例
3. 更新最佳实践
4. 添加验证规则
```

### 常见问题解决

1. 配置缺失：使用默认值和友好提示
2. 格式错误：添加详细的格式说明
3. 环境差异：使用条件配置
4. 敏感信息：使用环境变量或密钥管理服务