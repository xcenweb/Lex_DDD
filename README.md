# LexDDD - 词易Python基座

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-green.svg)](https://fastapi.tiangolo.com/)
[![Poetry](https://img.shields.io/badge/Poetry-Package%20Manager-blue)](https://python-poetry.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.38-red)](https://www.sqlalchemy.org/)

## 项目简介

[Github仓库地址(更新最快)](https://github.com/xcenweb/Lex_DDD)

LexDDD 是一个基于领域驱动设计（DDD）架构的后端开发基座。项目采用现代化的技术栈和架构设计，提供高性能、可维护和可扩展。

其实是实际项目开发过程中，偶然发现这部分可以作为开发基座，所以就把它开源出来。

文档见 [docs](./docs/README.md)

- 遵循PEP 8编码规范
- 使用类型注解
- 编写单元测试
- 保持领域层的纯粹性
- 遵循DDD设计原则

## 技术架构

### 领域驱动设计 (DDD)

项目严格遵循DDD架构原则，将系统分为以下核心层次：

- **领域层 (Domain Layer)**
  - 包含核心业务逻辑和实体
  - 定义领域模型和业务规则
  - 实现领域服务和值对象

- **应用层 (Application Layer)**
  - 协调领域对象以完成用例
  - 处理事务管理
  - 实现应用服务

- **基础设施层 (Infrastructure Layer)**
  - 提供技术实现
  - 处理数据持久化
  - 集成外部服务

- **接口层 (Interface Layer)**
  - 定义API接口
  - 处理请求响应
  - 实现路由管理

### 技术栈

- **Web框架**: FastAPI 0.115.8
- **ORM**: SQLAlchemy 2.0.38
- **数据库**: MySQL
- **包管理**: Poetry
- **API文档**: Swagger/OpenAPI

## 项目结构

```
src/
├── domain/          # 领域层：核心业务逻辑和实体
├── application/     # 应用层：用例和业务流程编排
├── infrastructure/  # 基础设施层：技术实现和外部服务集成
└── interfaces/      # 接口层：API接口和路由定义
```

## 环境配置

### 前置要求

- Python 3.11+
- Poetry
- MySQL

### 安装依赖

```bash
# 安装项目依赖
poetry install

# 更新依赖
poetry update
```

### 环境变量配置

创建 `.env` 文件并配置以下环境变量：

```env
# 调试模式
LEX_DEBUG=True

# 数据库设置
LEX_DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/lextrade
```

## 启动服务

```bash
# 启动开发服务器
uvicorn main:app --reload
```

启动后可访问：
- API文档：http://localhost:8000/docs
- 交互式API文档：http://localhost:8000/redoc

## 数据库模型

使用 SQLAlchemy 生成数据库模型：

```bash
sqlacodegen --outfile ./src/domain/models.py mysql://user:password@localhost:3306/lextrade
```

## TODO

未来想要支持的功能和改进：

- [x] 单元测试
- [x] logger日志
- [x] 更完善的异常处理
- [x] 更利于ai理解的 `file content prompt`

## 许可证

[Apache License 2.0](LICENSE)