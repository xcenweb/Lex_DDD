"""
系统配置
"""

from typing import Optional
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv(
    dotenv_path=".env", # .env文件路径
    verbose=False,      # 是否输出日志
    override=True,      # 是否覆盖系统中的环境变量
    interpolate=True,   # 是否对环境变量中的变量引用进行扩展
    encoding="utf8"     # 文件编码
)

class Settings():
    """应用配置类"""
    DEBUG: bool = os.getenv("LEX_DEBUG", "False").lower() == "true" # 调试模式开关

    DATABASE_URL: str = os.getenv("LEX_DATABASE_URL") # 数据库设置

    # 邮件服务配置
    SMTP_HOST: str = os.getenv("LEX_SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("LEX_SMTP_PORT"))
    SMTP_USERNAME: str = os.getenv("LEX_SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("LEX_SMTP_PASSWORD")
    SMTP_DEFAULT_SENDER: str = os.getenv("LEX_SMTP_DEFAULT_SENDER")
    SMTP_USE_PROTOCOL: str = os.getenv("LEX_SMTP_USE_PROTOCOL", "tls").lower()
    # 阿里云短信服务配置
    SMS_ACCESS_KEY_ID: str = os.getenv("LEX_SMS_ACCESS_KEY_ID")
    SMS_ACCESS_KEY_SECRET: str = os.getenv("LEX_SMS_ACCESS_KEY_SECRET")
    SMS_SIGN_NAME: str = os.getenv("LEX_SMS_SIGN_NAME")
    SMS_ENDPOINT: str = os.getenv("LEX_SMS_ENDPOINT", "dysmsapi.aliyuncs.com")

# 创建配置类实例
settings = Settings()
