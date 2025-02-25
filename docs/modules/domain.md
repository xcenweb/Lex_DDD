# 领域层 (Domain)

## 模块介绍

领域层是DDD架构的核心，包含业务的核心概念和规则：

- 定义业务实体和值对象
- 实现领域逻辑和规则
- 定义领域事件和服务
- 确保业务完整性

## 主要组件

### 实体 (Entities)

- 具有唯一标识
- 包含业务属性和行为
- 维护业务规则和约束
- 实现领域逻辑

### 值对象 (Value Objects)

- 描述领域特征
- 不可变性
- 无需唯一标识
- 基于属性比较相等性

### 聚合 (Aggregates)

- 定义数据一致性边界
- 确保业务规则完整性
- 管理实体间的关系
- 提供事务边界

### 领域服务 (Domain Services)

- 实现跨实体的业务逻辑
- 处理复杂的领域规则
- 协调多个聚合的操作

## 开发指南

### 设计原则

1. 领域模型应反映业务概念
2. 保持实体和值对象的不变性
3. 通过聚合维护一致性
4. 使用领域事件处理副作用

### AI提示词使用技巧

#### 创建实体

```
请帮我创建[实体名称]实体：
1. 定义属性和标识符
2. 实现业务方法
3. 添加验证规则
4. 设计不变量

示例：
class Order:
    def __init__(self, order_id: str, user_id: str, amount: Decimal):
        self.order_id = order_id
        self.user_id = user_id
        self.amount = amount
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
    
    def validate(self) -> None:
        if self.amount <= 0:
            raise ValueError("订单金额必须大于0")
```

#### 创建值对象

```
请帮我创建[值对象名称]：
1. 定义不可变属性
2. 实现相等性比较
3. 添加业务方法
4. 确保线程安全

示例：
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str
    
    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("货币类型不匹配")
        return Money(self.amount + other.amount, self.currency)
```

#### 定义聚合

```
请帮我设计[聚合名称]聚合：
1. 确定聚合根
2. 定义实体关系
3. 实现业务规则
4. 添加领域事件

示例：
class OrderAggregate:
    def __init__(self, order: Order):
        self.order = order
        self.items: List[OrderItem] = []
        self.events: List[DomainEvent] = []
    
    def add_item(self, item: OrderItem) -> None:
        if len(self.items) >= 100:
            raise ValueError("订单项不能超过100个")
        self.items.append(item)
        self.events.append(OrderItemAddedEvent(self.order.order_id, item))
```

### 最佳实践

1. 使用工厂方法创建复杂对象
2. 通过规约模式封装查询条件
3. 使用领域事件处理副作用
4. 保持聚合边界小而内聚
5. 通过值对象实现细粒度的领域概念