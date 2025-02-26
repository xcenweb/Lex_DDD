"""路由模块

包含所有API路由的定义
"""

from fastapi import APIRouter
from pathlib import Path
import importlib

# 创建根路由
router = APIRouter()

# 自动扫描并注册所有路由模块
def register_routers():
    # 获取当前目录路径
    current_dir = Path(__file__).parent
    
    # 遍历当前目录下的所有Python文件
    for route_file in current_dir.glob("*.py"):
        if route_file.stem == "__init__":
            continue
            
        # 导入路由模块
        module_path = f"{__package__}.{route_file.stem}"
        module = importlib.import_module(module_path)
        
        # 如果模块中定义了router对象，则注册它
        if hasattr(module, "router"):
            router.include_router(module.router)

# 注册所有路由
register_routers()