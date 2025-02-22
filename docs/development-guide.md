# LexDDD 开发规范

## 目录

- [代码风格规范](#代码风格规范)
- [DDD架构开发规范](#ddd架构开发规范)
- [Git提交规范](#git提交规范)
- [单元测试规范](#单元测试规范)

## 代码风格规范

### Python代码规范

1. **PEP 8规范**
   - 使用4个空格进行缩进
   - 每行代码不超过79个字符
   - 使用空行分隔函数和类
   - 在运算符前后使用空格

2. **命名规范**
   - 类名使用CamelCase命名法
   - 函数和变量使用snake_case命名法
   - 常量使用大写字母，用下划线分隔
   - 私有属性以单下划线开头

3. **类型注解**
   - 所有函数参数和返回值都必须添加类型注解
   - 使用typing模块中的类型
   ```python
   from typing import List, Optional
   
   def get_user_by_id(user_id: int) -> Optional[User]:
       pass
   ```

## DDD架构开发规范

### 领域层（Domain Layer）

1. **实体（Entity）**
   - 必须包含唯一标识
   - 实现相等性比较方法
   - 包含业务逻辑方法

2. **值对象（Value Object）**
   - 不可变
   - 没有唯一标识
   - 基于属性值判断相等性

3. **领域服务（Domain Service）**
   - 处理跨实体的业务逻辑
   - 保持无状态
   - 命名要体现业务含义

### 应用层（Application Layer）

1. **应用服务**
   - 实现用例
   - 协调领域对象
   - 不包含业务逻辑

2. **数据传输对象（DTO）**
   - 用于层间数据传输
   - 避免暴露领域模型

### 基础设施层（Infrastructure Layer）

1. **仓储实现**
   - 实现领域层定义的仓储接口
   - 处理数据持久化细节

2. **外部服务集成**
   - 封装第三方服务调用
   - 实现领域接口

## Git提交规范

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type类型

- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

### 示例

```
feat(user): 添加用户注册功能

- 实现用户注册接口
- 添加密码加密
- 添加邮箱验证

Resolves: #123
```

## 单元测试规范

### 测试文件组织

- 测试文件命名：`test_<module_name>.py`
- 测试类命名：`Test<ClassName>`
- 测试方法命名：`test_<method_name>_<scenario>`

### 测试原则

1. **单一职责**
   - 每个测试用例只测试一个功能点
   - 测试用例之间保持独立

2. **AAA模式**
   - Arrange（准备）：准备测试数据
   - Act（执行）：执行被测试的代码
   - Assert（断言）：验证测试结果

### 示例

```python
from unittest import TestCase

class TestUserService(TestCase):
    def setUp(self):
        self.user_service = UserService()

    def test_create_user_with_valid_data(self):
        # Arrange
        user_data = {
            "username": "test_user",
            "email": "test@example.com"
        }

        # Act
        user = self.user_service.create_user(user_data)

        # Assert
        self.assertIsNotNone(user)
        self.assertEqual(user.username, user_data["username"])
```

### 测试覆盖率要求

- 领域层：90%以上
- 应用层：80%以上
- 接口层：70%以上
- 基础设施层：60%以上

## 总结

遵循以上开发规范，可以：

1. 保持代码风格一致性
2. 确保DDD架构的正确实现
3. 维护清晰的版本历史
4. 保证代码质量和可测试性

开发团队成员必须严格遵守这些规范，确保项目的可维护性和可扩展性。