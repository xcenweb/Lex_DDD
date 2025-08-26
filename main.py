from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pathlib import Path
import importlib.util

from app.core.lifecycle import lifespan
from app.core.exceptions import setup_exception_handlers
from app.core.config import settings

app = FastAPI(
    title="LexTrade API",
    description="提示词分享、交易和测试平台的API服务",
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.DEBUG,

    docs_url=settings.DEBUG and "/docs" or None,
    redoc_url=settings.DEBUG and "/redoc" or None,
    openapi_url=settings.DEBUG and "/openapi.json" or None,
)

# 自动注册路由
def register_routers():
    api_path = Path(__file__).parent / "app" / "api"

    def register_router_from_file(file_path: Path, base_package: str):
        try:
            if file_path.name == "__init__.py":
                return
            relative_path = file_path.relative_to(api_path.parent)
            module_name = str(relative_path).replace("\\", ".").replace("/", ".").removesuffix(".py")
            spec = importlib.util.spec_from_file_location(module_name, str(file_path))
            if not spec:
                raise ImportError(f"无法为文件 {file_path} 创建模块规范")
            module = importlib.util.module_from_spec(spec)
            if not spec.loader:
                raise ImportError(f"模块 {module_name} 的加载器不存在")
            spec.loader.exec_module(module)
            if hasattr(module, "router"):
                app.include_router(module.router)
            else:
                print(f"警告: 模块 {module_name} 中未找到router对象")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"注册路由文件 {file_path} 时发生错误: {str(e)}")
    # 递归遍历所有Python文件
    try:
        if not api_path.exists():
            raise FileNotFoundError(f"API目录不存在: {api_path}")

        for route_file in api_path.rglob("*.py"):
            register_router_from_file(route_file, "app.api")
    except Exception as e:
        print(f"遍历API目录时发生错误: {str(e)}")

register_routers()

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置信任主机中间件
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "10.7.22.109"]
)

# 设置全局异常处理器
setup_exception_handlers(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5418,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )