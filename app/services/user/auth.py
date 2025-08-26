"""用户认证服务"""

import secrets
from datetime import datetime, timedelta
from typing import Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users, UserTokens

from app.services.verification import VerificationCodeService
from app.services.user.base import UserBaseService

class UserAuthService(UserBaseService):
    """用户认证服务"""

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
        self.verification_service = VerificationCodeService(db_session)

    async def login_with_email_vcode(self, target: str, vcode: str, client_info: Dict[str, str]) -> Dict[str, Any]:
        """使用邮箱验证码登录

        Args:
            target: 目标邮箱
            vcode: 验证码
            client_info: 客户端信息

        Returns:
            Dict: 用户信息和登录令牌

        Raises:
            ValueError: 验证码验证失败、用户不存在或已被封禁
        """
        # 验证验证码
        try:
            await self.verification_service.verify_code(target, vcode)
        except ValueError as e:
            raise ValueError(f"验证码验证失败: {str(e)}")

        # 获取用户
        user = await self._get_user_by_email(target)

        # 更新最后登录时间
        await self._update_last_login(user)

        # 生成登录令牌
        token_data = await self._generate_token(user.id, client_info)

        # 返回用户信息和令牌
        return {
            "user": self._format_user_info(user),
            "tokens": token_data
        }

    async def _validate_registration_data(self, nickname: str, password: str, target: str) -> None:
        """验证注册数据

        Args:
            nickname: 昵称
            password: 密码
            target: 目标邮箱

        Raises:
            ValueError: 验证失败信息
        """
        # 验证昵称长度
        if len(nickname) < 1 or len(nickname) > 15:
            raise ValueError("昵称长度必须在1-15个字符之间")

        # 验证密码长度
        if len(password) < 6 or len(password) > 20:
            raise ValueError("密码长度必须在6-20个字符之间")

        # 检查用户是否已存在
        if await self._check_email_exists(target):
            raise ValueError("该邮箱已被注册")

    async def register_with_email_vcode(self, nickname: str, password: str, avatar_path: str, target: str, vcode: str, client_info: Dict[str, str]) -> Dict[str, Any]:
        """使用邮箱验证码注册

        Args:
            nickname: 昵称
            password: 密码
            avatar_path: 头像路径
            target: 目标邮箱
            vcode: 验证码
            client_info: 客户端信息

        Returns:
            Dict: 用户信息和登录令牌

        Raises:
            ValueError: 验证码验证失败、验证数据失败
        """
        # 验证验证码
        try:
            await self.verification_service.verify_code(target, vcode)
        except ValueError as e:
            raise ValueError(f"验证码验证失败: {str(e)}")

        # 验证注册数据
        await self._validate_registration_data(nickname, password, target)

        # 创建新用户
        user = Users(
            nickname=nickname,
            password=self.get_password_hash(password),
            avatar_url=avatar_path,
            email=target,
            points=0,
            level=0,
            level_exp=0,
            favorites_count=0,
            follow_count=0,
            fans_count=0,
            prompt_count=0,
            status=1
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        # 生成登录令牌
        token_data = await self._generate_token(user.id, client_info)

        # 返回用户信息和令牌
        return {
            "user": self._format_user_info(user),
            "tokens": token_data
        }

    async def login_with_email_password(self, target: str, password: str, client_info: Dict[str, str]) -> Dict[str, Any]:
        """使用邮箱密码登录

        Args:
            target: 目标邮箱
            password: 密码
            client_info: 客户端信息

        Returns:
            Dict: 用户信息和登录令牌

        Raises:
            ValueError: 邮箱或密码错误、账号已被封禁
        """
        # 获取用户
        try:
            user = await self._get_user_by_email(target)
        except ValueError:
            raise ValueError("邮箱或密码错误")

        # 验证密码
        if not self.verify_password(user.password, password):
            raise ValueError("邮箱或密码错误")

        # 更新最后登录时间
        await self._update_last_login(user)

        # 生成登录令牌
        token_data = await self._generate_token(user.id, client_info)

        # 返回用户信息和令牌
        return {
            "user": self._format_user_info(user),
            "tokens": token_data
        }

    async def _generate_token(self, user_id: int, client_info: Dict[str, str]) -> Dict[str, Any]:
        """生成用户登录令牌

        Args:
            user_id: 用户ID
            client_info

        Returns:
            Dict: 令牌信息
        """
        # 生成令牌
        access_token = secrets.token_hex(64)
        refresh_token = secrets.token_hex(64)

        # 设置过期时间
        access_expires = datetime.utcnow() + timedelta(days=7)  # 访问令牌过期
        refresh_expires = datetime.utcnow() + timedelta(days=60)  # 刷新令牌过期

        # 查询用户是否已有令牌记录
        query = select(UserTokens).where(UserTokens.user_id == user_id)
        result = await self.db.execute(query)
        existing_token:UserTokens = result.scalar_one_or_none()

        if existing_token:
            # 更新现有令牌记录
            existing_token.access_token = access_token
            existing_token.refresh_token = refresh_token
            existing_token.access_expires_at = access_expires
            existing_token.refresh_expires_at = refresh_expires
            existing_token.device_info = client_info.get("device_info", "")
            existing_token.ipv4 = client_info.get("ipv4", "")
            existing_token.ipv6 = client_info.get("ipv6", "")
            token = existing_token
        else:
            # 创建新的令牌记录
            token = UserTokens(
                user_id=user_id,
                access_token=access_token,
                refresh_token=refresh_token,
                access_expires_at=access_expires,
                refresh_expires_at=refresh_expires,
                device_info=client_info.get("device_info", ""),
                ipv4=client_info.get("ipv4", ""),
                ipv6=client_info.get("ipv6", ""),
            )
            self.db.add(token)

        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": int(access_expires.timestamp()) # access_token的过期时间
        }

    async def logout(self, access_token: str) -> None:
        """退出登录

        Args:
            access_token: 访问令牌

        Raises:
            ValueError: 访问令牌无效
        """
        if not access_token:
            raise ValueError("访问令牌不能为空")

        # 查询访问令牌
        query = select(UserTokens).where(UserTokens.access_token == access_token)
        result = await self.db.execute(query)
        token_record = result.scalar_one_or_none()

        # 验证令牌是否存在
        if not token_record:
            raise ValueError("访问令牌无效")

        # 清除令牌记录
        await self.db.delete(token_record)
        await self.db.commit()

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """刷新访问令牌

        Args:
            refresh_token: 刷新令牌

        Returns:
            Dict: 新的令牌信息

        Raises:
            ValueError: 刷新令牌无效或已过期
        """
        # 查询刷新令牌
        query = select(UserTokens).where(UserTokens.refresh_token == refresh_token)
        result = await self.db.execute(query)
        token_record = result.scalar_one_or_none()

        # 验证令牌是否存在
        if not token_record:
            raise ValueError("刷新令牌无效")

        # 验证令牌是否过期
        if token_record.refresh_expires_at < datetime.utcnow():
            raise ValueError("刷新令牌已过期，请重新登录")

        # 生成新的访问令牌
        new_access_token = secrets.token_hex(64)

        # 设置新的过期时间
        new_access_expires = datetime.utcnow() + timedelta(days=7)  # 访问令牌过期时间

        # 更新令牌记录
        token_record.access_token = new_access_token
        token_record.access_expires_at = new_access_expires

        await self.db.commit()

        # 获取用户信息
        user = await self._get_user_by_id(token_record.user_id)

        # 返回新的令牌信息和用户信息
        return {
            "user": self._format_user_info(user),
            "tokens": {
                "access_token": new_access_token,
                "refresh_token": refresh_token,  # 保持原有的刷新令牌不变
                "expires_at": int(new_access_expires.timestamp())  # 新的访问令牌过期时间
            }
        }