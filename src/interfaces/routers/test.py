"""测试路由模块

用于测试系统功能的路由
"""

from fastapi import APIRouter, Depends
from src.infrastructure.email import EmailService
from src.infrastructure.config import settings
from src.interfaces.responses import create_response
import random
import string

router = APIRouter(prefix="/test", tags=["测试"])

# 创建EmailService实例
email_service = EmailService(
    smtp_host=settings.SMTP_HOST,
    smtp_port=settings.SMTP_PORT,
    username=settings.SMTP_USERNAME,
    password=settings.SMTP_PASSWORD,
    default_sender=settings.SMTP_DEFAULT_SENDER,
    use_tls=settings.SMTP_USE_TLS
)

def generate_verification_code(length: int = 6) -> str:
    """生成随机验证码

    Args:
        length: 验证码长度，默认6位

    Returns:
        str: 生成的验证码
    """
    return ''.join(random.choices(string.digits, k=length))

@router.post("/send-verification-code")
async def test_send_verification_code(email: str):
    """测试发送验证码邮件

    Args:
        email: 接收验证码的邮箱地址

    Returns:
        JSONResponse: 发送结果
    """
    try:
        # 生成6位随机验证码
        code = generate_verification_code()

        # 发送验证码邮件
        await email_service.send_verification_code(email, code)

        return create_response(
            message="验证码发送成功",
            data={"email": email}
        )
    except Exception as e:
        return create_response(
            status_code=500,
            message="验证码发送失败",
            detail=str(e)
        )