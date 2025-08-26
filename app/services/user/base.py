"""用户基础服务"""

from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users
import bcrypt

class UserBaseService:
    """用户基础服务"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    def get_password_hash(self, password: str) -> str:
        """获取加密后密码"""
        password = password.encode('utf-8')
        return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, hashed_password: str, password: str) -> bool:
        """验证加密后的密码"""
        password = password.encode('utf-8')
        return bcrypt.checkpw(password, hashed_password.encode('utf-8'))

    def _format_user_info(self, user: Users) -> Dict[str, Any]:
        """格式化用户信息

        Args:
            user: 用户对象

        Returns:
            Dict: 格式化后的用户信息
        """
        return {
            "id": user.id,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "email": user.email,
            "phone": user.phone,
            "bio": user.bio, # 个人简介

            "points": user.points,
            "level": user.level,
            "level_exp": user.level_exp,

            "count": {
                "favorites": user.favorites_count,
                "follow": user.follow_count,
                "fans": user.fans_count,
                "prompt": user.prompt_count,
            },

            "created_at": str(user.created_at),
            "last_login_at": str(user.last_login_at),
        }

    async def _get_user_by_email(self, email: str) -> Users:
        """通过邮箱获取用户

        Args:
            email: 用户邮箱

        Returns:
            Users: 用户对象

        Raises:
            ValueError: 用户不存在或已被删除
        """
        query = select(Users).where(Users.email == email, Users.is_deleted == 0)
        result = await self.db.execute(query)
        user: Optional[Users] = result.scalar_one_or_none()

        if not user:
            raise ValueError("邮箱不存在或错误")

        if user.status != 1:
            raise ValueError("账号已被封禁")

        return user

    async def _update_last_login(self, user: Users) -> None:
        """更新用户最后登录时间

        Args:
            user: 用户对象
        """
        user.last_login_at = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    async def _check_email_exists(self, email: str) -> bool:
        """检查邮箱是否已被注册

        Args:
            email: 用户邮箱

        Returns:
            bool: 邮箱是否已被注册
        """
        query = select(Users).where(Users.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None