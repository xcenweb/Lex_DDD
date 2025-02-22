"""
系统配置
"""

from typing import Optional
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv(
    dotenv_path=".env", #.env文件路径
    verbose=True,       #是否输出日志
    override=False,     # .env是否覆盖系统的环境变量
    interpolate=True,   # 是否对环境变量中的变量进行扩展
    encoding="utf8"     #.env文件编码
)

class Settings():
    """应用配置类"""
    DEBUG: bool = os.getenv("LEX_DEBUG") # 是否开启调试模式
    DATABASE_URL: str = os.getenv("LEX_DATABASE_URL") # 数据库设置

settings = Settings()

print(settings.DEBUG)