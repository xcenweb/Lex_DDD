"""
系统配置
"""

from typing import Optional
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv(
    dotenv_path=".config", # .env文件路径
    verbose=False,      # 是否输出日志
    override=True,      # 是否覆盖系统中的环境变量
    interpolate=True,   # 是否对环境变量中的变量引用进行扩展
    encoding="utf-8"     # 文件编码
)

class Settings():
    """
    基础配置
    """
    DEBUG: bool = os.getenv("LEX_DEBUG", "False").lower() == "true" # 调试模式开关
    DATABASE_URL: str = os.getenv("LEX_DATABASE_URL") # 数据库设置

class SMTP():
    """
    邮件服务配置
    """
    HOST: str = os.getenv("LEX_SMTP_HOST")
    PORT: int = int(os.getenv("LEX_SMTP_PORT"))
    USERNAME: str = os.getenv("LEX_SMTP_USERNAME")
    PASSWORD: str = os.getenv("LEX_SMTP_PASSWORD")
    DEFAULT_SENDER: str = os.getenv("LEX_SMTP_DEFAULT_SENDER")
    PROTOCOL: str = os.getenv("LEX_SMTP_USE_PROTOCOL", "tls").lower()

class SMS():
    """
    短信服务配置
    """
    ACCESS_KEY_ID: str = os.getenv("LEX_SMS_ACCESS_KEY_ID")
    ACCESS_KEY_SECRET: str = os.getenv("LEX_SMS_ACCESS_KEY_SECRET")
    SIGN_NAME: str = os.getenv("LEX_SMS_SIGN_NAME")

# 实例化配置类
settings = Settings()
sms = SMS()
smtp = SMTP()