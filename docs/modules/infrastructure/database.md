# 数据库模块

## 模块介绍

数据库模块(`database.py`)是基础设施层的核心组件之一，负责管理数据库连接、会话和ORM操作。该模块基于SQLAlchemy实现，提供了异步数据库操作支持。

## 功能特性

- 异步数据库连接管理
- 会话工厂模式实现
- 事务管理支持
- 连接池配置
- 数据库迁移工具集成

## 配置说明

数据库配置项在`.env`文件中定义：

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

## 使用示例

### 基本用法

```python
from infrastructure.database import get_session

async with get_session() as session:
    result = await session.execute(query)
    await session.commit()
```

### 事务管理

```python
from infrastructure.database import transaction

@transaction
async def create_user(session, user_data):
    user = User(**user_data)
    session.add(user)
    return user
```

## AI提示词使用技巧

### 1. 创建数据库操作

提示词模板：
```
请帮我实现以下数据库操作：
1. 表名：[表名]
2. 操作类型：[增/删/改/查]
3. 条件：[查询条件]
4. 需要处理的字段：[字段列表]
5. 是否需要事务支持
```

示例：
```
请帮我实现以下数据库操作：
1. 表名：users
2. 操作类型：查询
3. 条件：按用户状态筛选
4. 需要处理的字段：id, username, status
5. 不需要事务支持
```

### 2. 优化查询性能

提示词模板：
```
请帮我优化以下查询性能：
[原始查询代码]

优化要求：
1. 添加必要的索引
2. 优化查询语句
3. 考虑缓存策略
```

### 3. 实现复杂查询

提示词模板：
```
请帮我实现以下复杂查询：
1. 涉及表：[表名列表]
2. 关联条件：[表间关系]
3. 查询条件：[筛选条件]
4. 排序要求：[排序规则]
5. 分页参数：[页码/每页数量]
```

## 最佳实践

1. 始终使用异步会话管理器
2. 适当设置连接池大小
3. 使用事务装饰器管理事务
4. 定期清理过期连接
5. 实现数据库健康检查

## 常见问题

1. **连接池耗尽**
   - 原因：并发请求过多
   - 解决：调整池大小和超时设置

2. **死锁处理**
   - 原因：事务冲突
   - 解决：实现重试机制

3. **连接泄漏**
   - 原因：未正确释放连接
   - 解决：使用上下文管理器

## 注意事项

1. 避免长事务
2. 合理使用索引
3. 定期维护数据库
4. 监控连接池状态
5. 实现错误重试机制