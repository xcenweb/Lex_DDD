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
        use_protocol: str = "tls"
    ):
        """初始化邮件服务

        Args:
            smtp_host: SMTP服务器地址
            smtp_port: SMTP服务器端口
            username: SMTP认证用户名
            password: SMTP认证密码
            default_sender: 默认发件人
            use_protocol: 使用的加密协议（tls或ssl）
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.default_sender = default_sender or username
        self.use_protocol = use_protocol.lower()

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
        if self.use_protocol == 'ssl':
            # 使用SSL连接
            async with aiosmtplib.SMTP(hostname=self.smtp_host, port=self.smtp_port, use_tls=True) as server:
                await server.login(self.username, self.password)
                await server.send_message(msg)
        else:
            # 使用普通连接或TLS
            async with aiosmtplib.SMTP(hostname=self.smtp_host, port=self.smtp_port) as server:
                if self.use_protocol == 'tls':
                    await server.starttls()
                await server.login(self.username, self.password)
                await server.send_message(msg)