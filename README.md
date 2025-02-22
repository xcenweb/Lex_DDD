采用DDD架构的基础框架，非常好的ai适应性，可用于ai快速开发后端

`微信交流群：wx_0xbcyuncen`

使用poetry作为包管理工具，默认支持 `.env` 环境变量配置

## 项目架构

项目采用领域驱动设计（DDD）架构，分为以下几层：

```
src/
├── domain/          # 领域层：核心业务逻辑和实体
├── application/     # 应用层：用例和业务流程编排
├── infrastructure/  # 基础设施层：技术实现和外部服务集成
└── interfaces/      # 接口层：API接口和路由定义
```

### 分层说明

1. **领域层 (Domain Layer)**
   - 定义核心业务实体和值对象
   - 实现领域服务和业务规则
   - 定义仓储接口

2. **应用层 (Application Layer)**
   - 实现应用服务和用例
   - 协调领域对象
   - 处理事务和业务流程

3. **基础设施层 (Infrastructure Layer)**
   - 实现持久化机制
   - 提供外部服务集成
   - 处理技术细节（日志、缓存等）

4. **接口层 (Interfaces Layer)**
   - 提供API接口
   - 处理请求和响应
   - 实现路由和控制器

## 技术栈

### 后端框架和工具
- **Web框架**：FastAPI 0.115.x
  - 高性能异步API框架
  - 自动API文档生成
  - 请求验证和序列化

- **数据库和ORM**
  - MySQL 5.6+
  - SQLAlchemy 2.0+ (异步ORM)

- **依赖管理**
  - Poetry（包管理和虚拟环境）
  - Python 3.11+

### 开发工具和规范

- **API文档**
  - Swagger UI（/docs）
  - ReDoc（/redoc）
