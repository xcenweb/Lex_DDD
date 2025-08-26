import random
import string
from typing import Optional, Tuple
from datetime import datetime, timedelta

import email_validator

from sqlalchemy import select, and_, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import smtp
from app.utils import email
from app.models import VerificationCodes

class VerificationCodeService:
    """验证码服务"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.email_util = email.EmailUtil(
            smtp_host=smtp.HOST,
            smtp_port=smtp.PORT,
            username=smtp.USERNAME,
            password=smtp.PASSWORD,
            use_protocol=smtp.PROTOCOL,
        )

    @staticmethod
    def generate_code(length: int = 6):
        """生成指定长度的随机验证码"""
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    def is_email(target: str) -> bool:
        try:
            email_validator.validate_email(target)
            return True
        except email_validator.EmailNotValidError:
            return False

    @staticmethod
    def normalize_email(email: str):
        """
        规范化邮箱地址
        """
        try:
            email_address = email_validator.validate_email(email)
            return email_address.email
        except email_validator.EmailNotValidError:
            raise ValueError("无效的邮箱地址")

    async def create_code(self, target: str, name: str, expires_in: int = 600) -> str:
        """创建新的邮箱验证码

        Args:
            target: 目标邮箱
            name: 验证码名称 (如: 注册、登录、修改密码等)
            expires_in: 过期时间(秒)，默认10分钟

        Returns:
            str: 生成的验证码
        """

        if not self.is_email(target):
            raise ValueError("请输入有效的邮箱地址")

        target = self.normalize_email(target)

        verification = VerificationCodes(
            target=target,
            type=2,  # 邮箱验证码
            code=self.generate_code(),
            expired_at=datetime.utcnow() + timedelta(seconds=expires_in),
            created_at=datetime.utcnow(),
            is_used=0
        )

        self.db.add(verification)
        await self.db.commit()

        await self.email_util.send_verification_code(to_addr=target, code=verification.code, subject=name)

        return True

    async def verify_code(self, target: str, code: str):
        """校验验证码

        Args:
            target: 目标邮箱
            code: 验证码
        """

        if not self.is_email(target):
            raise ValueError("请输入有效的邮箱地址")

        target = self.normalize_email(target)

        query = select(VerificationCodes).where(
            and_(
                VerificationCodes.target == target,
                VerificationCodes.code == code,
                VerificationCodes.expired_at > datetime.utcnow(),
                VerificationCodes.is_used == 0
            )
        )
        # 查询验证码
        verification = await self.db.execute(query)
        verification = verification.scalar_one_or_none()

        if not verification:
            raise ValueError("验证码不存在或已过期")

        verification.is_used = 1 # 标记验证码为已使用
        await self.db.commit()

        return True

    async def clean_codes(self) -> int:
        """删除过期的验证码

        Returns:
            int: 清理的记录数量
        """
        query = delete(VerificationCodes).where(
            or_(
                VerificationCodes.expired_at < datetime.utcnow(),
                VerificationCodes.is_used == 1
            )
        )

        result = await self.db.execute(query)
        await self.db.commit()

        return result.rowcount
