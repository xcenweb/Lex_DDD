# LexTrade Backend

## 项目介绍

LexDDD 是一个基于Python的后端框架，采用领域驱动设计（DDD）架构。他的优点是能让你不用太多语言就能开发理论上安全的、规范的项目

## 项目特点

- 基于DDD架构，代码结构清晰，易于维护
- 完善的异常处理机制
- 集成日志系统，便于问题追踪
- 完整的单元测试覆盖
- AI友好的开发流程

## 快速开始

### 环境要求

- Python 3.8+
- Poetry

### 安装依赖

```bash
poetry install
```

### 运行项目

```bash
poetry run python main.py
```

## AI开发指南

本项目支持通过AI辅助进行开发。以下是一些常用的AI提示词模板及其示例结果：

### 项目开场白

```
欢迎使用LexTrade Backend项目！本文档将帮助您（或AI助手）快速理解项目架构、业务领域和开发规范。

#### 技术栈

- **Web框架**：FastAPI - 高性能异步Web框架
- **ORM**：SQLAlchemy - 功能强大的数据库ORM工具
- **数据验证**：Pydantic - 数据模型验证和序列化
- **测试框架**：Pytest - 现代化的Python测试工具

#### DDD架构说明

项目严格遵循DDD（领域驱动设计）架构，各层职责如下：

1. **领域层（Domain）**
   - 定义核心业务实体和值对象
   - 实现领域服务和领域事件
   - 定义仓储接口

2. **应用层（Application）**
   - 编排领域对象
   - 处理业务用例
   - 实现事务管理

3. **基础设施层（Infrastructure）**
   - 提供技术实现
   - 实现仓储接口
   - 集成外部服务

4. **接口层（Interfaces）**
   - 处理HTTP请求
   - 实现API接口
   - 处理用户认证

#### 核心业务领域

1. **交易管理**
   - 订单创建和管理
   - 交易执行和监控
   - 风险控制

2. **用户管理**
   - 用户认证和授权
   - 账户管理
   - 权限控制

3. **资产管理**
   - 资金账户
   - 持仓管理
   - 资产统计

#### 开发规范

1. **代码风格**
   - 遵循PEP 8规范
   - 使用类型注解
   - 编写详细的文档字符串

2. **架构规范**
   - 严格遵循DDD分层架构
   - 保持层间依赖的单向性
   - 使用依赖注入管理对象

3. **测试规范**
   - 单元测试覆盖率>80%
   - 编写集成测试
   - 使用测试夹具管理测试数据

4. **异常处理**
   - 定义业务异常类型
   - 统一异常处理机制
   - 详细的错误日志记录

#### 项目结构

```
src/
├── domain/          # 领域层：包含核心业务逻辑
├── application/     # 应用层：处理用例和业务流程
├── infrastructure/  # 基础设施层：提供技术实现
└── interfaces/      # 接口层：处理外部请求

配置文件：
- pyproject.toml     # Poetry依赖管理
- .env.example       # 环境变量模板
- config.py         # 应用配置
```
```

### 新功能开发

示例提示词：
```
请帮我在交易模块中实现订单创建功能：
1. 遵循DDD架构原则
2. 包含必要的异常处理
3. 添加相应的单元测试
4. 确保代码风格符合项目规范
```

示例结果：
```python
# domain/order.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Order:
    id: str
    user_id: str
    amount: float
    status: str
    created_at: datetime

    def validate(self) -> None:
        if self.amount <= 0:
            raise ValueError("订单金额必须大于0")

# application/order_service.py
class OrderService:
    def create_order(self, user_id: str, amount: float) -> Order:
        try:
            order = Order(
                id=generate_order_id(),
                user_id=user_id,
                amount=amount,
                status="pending",
                created_at=datetime.now()
            )
            order.validate()
            return self.order_repository.save(order)
        except Exception as e:
            logger.error(f"创建订单失败：{str(e)}")
            raise OrderCreationError(str(e))

# test/test_order.py
def test_create_order():
    service = OrderService()
    order = service.create_order("user123", 100.0)
    assert order.user_id == "user123"
    assert order.amount == 100.0
    assert order.status == "pending"
```

### 代码优化

示例提示词：
```
请帮我优化以下订单查询代码：

def get_user_orders(user_id):
    orders = db.query("SELECT * FROM orders WHERE user_id = %s", user_id)
    return orders

要求：
1. 提高性能
2. 增强可读性
3. 完善错误处理
4. 添加必要的注释
```

示例结果：
```python
from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Order

def get_user_orders(
    user_id: str,
    session: Session,
    limit: Optional[int] = 100
) -> List[Order]:
    """获取用户订单列表

    Args:
        user_id: 用户ID
        session: 数据库会话
        limit: 返回结果数量限制

    Returns:
        List[Order]: 订单列表

    Raises:
        DatabaseError: 数据库查询异常
    """
    try:
        # 使用索引优化查询性能
        return session.query(Order)\
            .filter(Order.user_id == user_id)\
            .order_by(Order.created_at.desc())\
            .limit(limit)\
            .all()
    except Exception as e:
        logger.error(f"查询用户{user_id}的订单失败：{str(e)}")
        raise DatabaseError(f"订单查询失败：{str(e)}")
```

## 文档导航

- [架构设计](architecture.md) - 了解项目的整体架构
- [模块文档](modules/) - 查看各模块的详细说明
- [AI提示词指南](ai-prompts.md) - 更多AI开发相关内容
- [常见问题](faq.md) - 解答常见问题