from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.lifecycle import lifespan
from src.infrastructure.exceptions import setup_exception_handlers
from src.infrastructure.config import settings

app = FastAPI(
    title="LexTrade API",
    description="提示词分享、交易和测试平台的API服务",
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.DEBUG,

    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 设置全局异常处理器
setup_exception_handlers(app)

@app.get("/")
async def root():
    """
    根路径
    """
    # 测试报错
    1/0
    return {"message": "欢迎使用LexTrade API服务"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5418, reload=True)
