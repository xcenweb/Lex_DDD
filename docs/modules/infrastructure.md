# 基础设施层 (Infrastructure)

## 模块介绍

基础设施层提供技术实现和外部服务集成：

- 实现持久化和数据访问
- 提供外部服务集成
- 处理技术细节和配置
- 支持跨切面关注点

## 主要组件

### 数据访问 (Data Access)

- 实现仓储接口
- 管理数据库连接
- 处理数据映射
- 优化查询性能

### 外部服务 (External Services)

- 集成第三方API
- 处理消息队列
- 实现缓存服务
- 管理外部资源

### 配置管理 (Configuration)

- 加载系统配置
- 管理环境变量
- 处理配置加密
- 维护配置一致性

## 开发指南

### 设计原则

1. 依赖倒置原则
2. 关注点分离
3. 单一职责原则
4. 接口隔离原则

### AI提示词使用技巧

#### 实现仓储

```
提示词：
请帮我实现订单(Order)的仓储：
1. 定义仓储接口
2. 实现数据映射
3. 添加CRUD操作
4. 优化查询性能

AI响应：
好的，我来帮您实现订单仓储。首先创建抽象仓储接口，然后实现具体的订单仓储类：

1. 仓储接口定义：

from abc import ABC, abstractmethod
from typing import Optional, List

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    def find_all(self) -> List[Order]:
        pass

    @abstractmethod
    def delete(self, order_id: str) -> None:
        pass

2. 具体实现：

from sqlalchemy.orm import Session
from typing import Optional, List

class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, order: Order) -> Order:
        try:
            order_model = OrderModel.from_entity(order)
            self.session.add(order_model)
            self.session.commit()
            return order_model.to_entity()
        except Exception as e:
            self.session.rollback()
            raise RepositoryError(f"保存订单失败：{str(e)}")

    def find_by_id(self, order_id: str) -> Optional[Order]:
        try:
            order_model = self.session.query(OrderModel)\
                .filter(OrderModel.order_id == order_id)\
                .first()
            return order_model.to_entity() if order_model else None
        except Exception as e:
            raise RepositoryError(f"查询订单失败：{str(e)}")

    def find_all(self) -> List[Order]:
        try:
            order_models = self.session.query(OrderModel).all()
            return [model.to_entity() for model in order_models]
        except Exception as e:
            raise RepositoryError(f"查询所有订单失败：{str(e)}")

    def delete(self, order_id: str) -> None:
        try:
            self.session.query(OrderModel)\
                .filter(OrderModel.order_id == order_id)\
                .delete()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise RepositoryError(f"删除订单失败：{str(e)}")
```

#### 配置外部服务

```
提示词：
请帮我实现邮件服务(EmailService)的配置：
1. 定义配置模型
2. 加载配置文件
3. 处理环境变量
4. 实现服务连接

AI响应：
好的，我来帮您实现邮件服务的配置。我们将使用pydantic来处理配置，并实现一个邮件服务类：

1. 配置模型：

from pydantic import BaseSettings, Field
from typing import Optional

class EmailConfig(BaseSettings):
    smtp_host: str
    smtp_port: int
    username: str
    password: str = Field(secrets=True)
    tls_enabled: bool = True
    timeout: int = 30

    class Config:
        env_prefix = "EMAIL_"
        env_file = ".env"

2. 服务实现：

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from typing import List, Optional

class EmailService:
    def __init__(self, config: EmailConfig):
        self.config = config
        self.client = self._create_client()

    def _create_client(self) -> smtplib.SMTP:
        client = smtplib.SMTP(
            host=self.config.smtp_host,
            port=self.config.smtp_port,
            timeout=self.config.timeout
        )
        if self.config.tls_enabled:
            client.starttls()
        client.login(self.config.username, self.config.password)
        return client

    def send_email(self, to: List[str], subject: str, body: str,
                   cc: Optional[List[str]] = None) -> None:
        try:
            message = MIMEMultipart()
            message["From"] = self.config.username
            message["To"] = ", ".join(to)
            if cc:
                message["Cc"] = ", ".join(cc)
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            recipients = to + (cc or [])
            self.client.send_message(message, to=recipients)
        except Exception as e:
            raise EmailError(f"发送邮件失败：{str(e)}")
```

### 最佳实践

1. 使用连接池优化性能
2. 实现重试和熔断机制
3. 添加监控和日志记录
4. 使用缓存提升性能
5. 实现异步操作处理