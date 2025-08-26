"""邮件服务模块

提供邮件发送功能，支持HTML内容和附件。用于系统通知、验证码等场景。
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import aiosmtplib

from typing import List, Optional, Dict, Any
from pathlib import Path

class EmailUtil:
    """邮件服务类"""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        default_sender: str = None,
        use_protocol: str = "tls",
        templates_dir: str = "data/templates/email"
    ):
        """初始化邮件服务

        Args:
            smtp_host: SMTP服务器地址
            smtp_port: SMTP服务器端口
            username: SMTP认证用户名
            password: SMTP认证密码
            default_sender: 默认发件人
            use_protocol: 使用的加密协议（tls或ssl）
            templates_dir: 邮件模板目录
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.default_sender = default_sender or username
        self.use_protocol = use_protocol.lower()
        self.templates_dir = Path(templates_dir)

    def load_and_render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """加载并渲染邮件模板

        Args:
            template_name: 模板文件名
            context: 模板变量

        Returns:
            str: 渲染后的内容

        Raises:
            FileNotFoundError: 模板文件不存在时抛出
        """
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")

        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        for key, value in context.items():
            template = template.replace(f"{{{key}}}", str(value))
        return template

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

    async def send_verification_code(self, to_addr: str, code: str, subject: str) -> None:
        """发送验证码邮件

        Args:
            to_addr: 收件人邮箱
            code: 验证码
            subject: 邮件主题
        """
        content = self.load_and_render_template('verification_code.html', {'code': code, 'exp': 10})
        await self.send_email(
            to_addrs=[to_addr],
            subject=subject,
            content=content,
            html=True
        )