"""邮件服务模块

提供邮件发送功能，支持HTML内容和附件。用于系统通知、验证码等场景。
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import aiosmtplib
from typing import List, Optional
from pathlib import Path

class EmailService:
    """邮件服务类"""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        default_sender: str = None,
        use_tls: bool = True
    ):
        """初始化邮件服务

        Args:
            smtp_host: SMTP服务器地址
            smtp_port: SMTP服务器端口
            username: SMTP认证用户名
            password: SMTP认证密码
            default_sender: 默认发件人
            use_tls: 是否使用TLS加密
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.default_sender = default_sender or username
        self.use_tls = use_tls

    async def send_email(
        self,
        to_addrs: List[str],
        subject: str,
        content: str,
        html: bool = False,
        sender: str = None,
        attachments: List[Path] = None
    ) -> None:
        """发送邮件

        Args:
            to_addrs: 收件人列表
            subject: 邮件主题
            content: 邮件内容
            html: 是否为HTML内容
            sender: 发件人，不指定则使用默认发件人
            attachments: 附件列表
        """
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = formataddr(('LexTrade', sender or self.default_sender))
        msg['To'] = ', '.join(to_addrs)

        # 设置邮件内容
        content_type = 'html' if html else 'plain'
        msg.attach(MIMEText(content, content_type, 'utf-8'))

        # 添加附件
        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as f:
                    part = MIMEText(f.read(), 'base64', 'utf-8')
                    part['Content-Type'] = 'application/octet-stream'
                    part['Content-Disposition'] = f'attachment; filename="{attachment.name}"'
                    msg.attach(part)

        # 发送邮件
        async with aiosmtplib.SMTP(hostname=self.smtp_host, port=self.smtp_port) as server:
            if self.use_tls:
                await server.starttls()
            await server.login(self.username, self.password)
            await server.send_message(msg)

    async def send_verification_code(
        self,
        to_addr: str,
        code: str,
        expire_minutes: int = 10
    ) -> None:
        """发送验证码邮件

        Args:
            to_addr: 收件人邮箱
            code: 验证码
            expire_minutes: 验证码有效期（分钟）
        """
        subject = 'LexTrade验证码'
        content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333;">验证码</h2>
            <p style="color: #666;">您的验证码是：</p>
            <div style="background-color: #f5f5f5; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; color: #333; margin: 20px 0;">
                {code}
            </div>
            <p style="color: #999; font-size: 14px;">验证码有效期为{expire_minutes}分钟，请尽快使用。</p>
            <p style="color: #999; font-size: 14px;">如果这不是您的操作，请忽略此邮件。</p>
        </div>
        """
        await self.send_email([to_addr], subject, content, html=True)