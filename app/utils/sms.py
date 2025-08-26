"""短信服务模块

提供短信发送功能，基于阿里云短信服务。用于验证码、通知等场景。
"""

import json
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_dysmsapi20170525.models import SendSmsRequest, QuerySendDetailsRequest
from alibabacloud_tea_openapi.models import Config

class SmsUtil:
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
        # 存储验证码信息，格式为 {phone: (code, expiry_time)}
        self._verification_codes = {}

    async def send_sms(
        self,
        phone_numbers: List[str],
        template_code: str,
        template_param: Optional[Dict[str, str]] = None
    ) -> str:
        """发送短信

        Args:
            phone_numbers: 手机号码列表
            template_code: 短信模板ID
            template_param: 模板参数（JSON格式）

        Returns:
            str: 发送回执ID
        """
        request = SendSmsRequest(
            phone_numbers=','.join(phone_numbers),
            sign_name=self.sign_name,
            template_code=template_code,
            template_param=json.dumps(template_param) if template_param else None
        )

        try:
            response = await self.client.send_sms_async(request)
            return response.body.bizId
        except Exception as e:
            # 这里可以添加更详细的错误处理逻辑
            raise Exception(f"发送短信失败: {str(e)}")

    async def generate_verification_code(self, length: int = 6) -> str:
        """生成验证码

        Args:
            length: 验证码长度，默认6位

        Returns:
            str: 生成的验证码
        """
        return ''.join(random.choices(string.digits, k=length))

    async def send_verification_code(
        self,
        phone: str,
        code: Optional[str] = None,
        template_id: str = "VERIFY_CODE",
        expire_minutes: int = 5
    ) -> str:
        """发送验证码短信

        Args:
            phone: 手机号码
            code: 验证码，如果为None则自动生成
            template_id: 短信模板ID
            expire_minutes: 验证码有效期（分钟）

        Returns:
            str: 验证码
        """
        if code is None:
            code = await self.generate_verification_code()

        # 存储验证码和过期时间
        expiry_time = datetime.now() + timedelta(minutes=expire_minutes)
        self._verification_codes[phone] = (code, expiry_time)

        # 发送验证码短信
        await self.send_sms(
            phone_numbers=[phone],
            template_code=template_id,
            template_param={"code": code}
        )

        return code

    async def verify_code(self, phone: str, code: str) -> bool:
        """验证短信验证码

        Args:
            phone: 手机号码
            code: 用户输入的验证码

        Returns:
            bool: 验证结果，True为验证通过
        """
        if phone not in self._verification_codes:
            return False

        stored_code, expiry_time = self._verification_codes[phone]

        # 验证码过期检查
        if datetime.now() > expiry_time:
            # 删除过期验证码
            del self._verification_codes[phone]
            return False

        # 验证码匹配检查
        if stored_code != code:
            return False

        # 验证成功后删除验证码
        del self._verification_codes[phone]
        return True

    async def send_template_message(
        self,
        phone: str,
        template_id: str,
        template_params: Dict[str, str]
    ) -> str:
        """发送模板消息

        Args:
            phone: 手机号码
            template_id: 模板ID
            template_params: 模板参数

        Returns:
            str: 发送回执ID
        """
        return await self.send_sms(
            phone_numbers=[phone],
            template_code=template_id,
            template_param=template_params
        )

    async def query_send_status(self, biz_id: str, phone_number: str) -> Dict:
        """查询短信发送状态

        Args:
            biz_id: 发送回执ID
            phone_number: 手机号码

        Returns:
            Dict: 发送状态信息
        """
        request = QuerySendDetailsRequest(
            biz_id=biz_id,
            phone_number=phone_number,
            send_date=datetime.now().strftime("%Y%m%d"),
            page_size=10,
            current_page=1
        )

        try:
            response = await self.client.query_send_details_async(request)
            return response.body.to_map()
        except Exception as e:
            raise Exception(f"查询短信状态失败: {str(e)}")
