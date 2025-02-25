"""短信服务模块

提供短信发送功能，基于阿里云短信服务。用于验证码、通知等场景。
"""

from typing import Dict, List, Optional
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_dysmsapi20170525.models import SendSmsRequest

class SmsService:
    """短信服务类"""

    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        sign_name: str,
        endpoint: str = "dysmsapi.aliyuncs.com"
    ):
        """初始化短信服务

        Args:
            access_key_id: 阿里云访问密钥ID
            access_key_secret: 阿里云访问密钥密码
            sign_name: 短信签名
            endpoint: 服务接入点
        """
        self.sign_name = sign_name
        self.client = Client(
            Config(
                access_key_id=access_key_id,
                access_key_secret=access_key_secret,
                endpoint=endpoint
            )
        )

    async def send_sms(
        self,
        phone_numbers: List[str],
        template_code: str,
        template_param: Optional[Dict[str, str]] = None
    ) -> None:
        """发送短信

        Args:
            phone_numbers: 手机号码列表
            template_code: 短信模板ID
            template_param: 模板参数（JSON格式）
        """
        request = SendSmsRequest(
            phone_numbers=','.join(phone_numbers),
            sign_name=self.sign_name,
            template_code=template_code,
            template_param=str(template_param) if template_param else None
        )

        try:
            await self.client.send_sms_async(request)
        except Exception as e:
            # 这里可以添加更详细的错误处理逻辑
            raise Exception(f"发送短信失败: {str(e)}")
