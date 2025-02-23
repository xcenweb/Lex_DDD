"""领域层 (Domain Layer)

该层包含业务的核心概念和规则：
1. 实体（Entities）：具有唯一标识的对象
2. 值对象（Value Objects）：无需唯一标识的对象
3. 聚合（Aggregates）：实体和值对象的组合
4. 领域服务（Domain Services）：跨实体的业务逻辑
5. 仓储接口（Repository Interfaces）：持久化抽象

"""