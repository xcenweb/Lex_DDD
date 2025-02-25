# 应用层 (Application)

## 模块介绍

应用层是DDD架构中的重要组成部分，主要负责：

- 协调领域对象和领域服务
- 实现业务用例和工作流
- 处理事务和应用服务
- 转换数据格式，适配外部接口

## 主要组件

### 应用服务 (Application Services)

- 实现具体的业务用例
- 协调多个领域对象和服务
- 管理事务边界
- 处理权限和验证

### 数据传输对象 (DTOs)

- 定义数据传输格式
- 实现数据转换和映射
- 隔离外部接口和内部模型
- 优化网络传输效率

## 开发指南

### 设计原则

1. 保持应用服务轻量级
2. 不包含业务规则
3. 使用事务脚本模式
4. 处理跨领域的协调

### AI提示词使用技巧

#### 创建应用服务

```
请帮我创建[业务名称]的应用服务：
1. 定义服务接口和方法
2. 实现用例流程
3. 添加事务管理
4. 处理异常情况
5. 实现数据转换

示例：
class OrderApplicationService:
    def __init__(self, order_repository: OrderRepository,
                 payment_service: PaymentService):
        self.order_repository = order_repository
        self.payment_service = payment_service
    
    @transactional
    def create_order(self, order_dto: OrderCreateDTO) -> OrderDTO:
        try:
            # 创建订单实体
            order = Order(
                user_id=order_dto.user_id,
                amount=order_dto.amount
            )
            order.validate()
            
            # 保存订单
            saved_order = self.order_repository.save(order)
            
            # 处理支付
            self.payment_service.process_payment(saved_order)
            
            # 转换为DTO返回
            return OrderDTO.from_entity(saved_order)
        except Exception as e:
            logger.error(f"创建订单失败：{str(e)}")
            raise ApplicationError("订单创建失败")
```

#### 实现数据转换

```
请帮我创建[实体名称]的DTO：
1. 定义数据结构
2. 添加验证规则
3. 实现转换方法
4. 处理嵌套对象

示例：
@dataclass
class OrderDTO:
    order_id: str
    user_id: str
    amount: Decimal
    status: str
    created_at: datetime
    
    @classmethod
    def from_entity(cls, order: Order) -> "OrderDTO":
        return cls(
            order_id=order.order_id,
            user_id=order.user_id,
            amount=order.amount,
            status=order.status.value,
            created_at=order.created_at
        )
```

### 最佳实践

1. 使用依赖注入管理服务依赖
2. 统一异常处理和日志记录
3. 实现幂等性和并发控制
4. 使用DTO验证请求数据
5. 合理划分事务边界