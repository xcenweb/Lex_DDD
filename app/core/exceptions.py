"""异常处理模块

统一处理FastAPI、Starlette和SQLAlchemy的异常
"""
import traceback

from typing import Dict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

from app.core.config import settings
from app.core.responses import create_response


def setup_exception_handlers(app: FastAPI) -> None:
    """设置全局异常处理器

    在生产、开发测试环境下接管所有异常，在调试模式下保持原始错误处理行为
    """

    @app.exception_handler(403)
    async def forbidden_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """处理403错误"""
        return create_response(code=403, message="非法访问")

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """处理404错误"""
        return create_response(code=404, message="请求的资源不存在")

    @app.exception_handler(405)
    async def method_not_allowed_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """处理405错误"""
        return create_response(code=405, message="非法请求")

    @app.exception_handler(429)
    async def too_many_requests_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """处理429错误"""
        return create_response(429, message="业务异常")

    # 在调试模式下不接管以下异常
    if settings.DEBUG:
        return

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """处理请求参数验证错误"""
        return create_response(code=422, message="请求参数验证失败")

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        """处理数据库相关错误"""
        return create_response(code=500, message="业务异常")

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """处理HTTP异常"""
        return create_response(exc.status_code, message=exc.detail)

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """处理所有未被捕获的异常"""
        return create_response(500, message="服务器错误")

def format_errors(errors: list) -> list:
    """格式化验证错误信息"""
    return [{
        "loc": error["loc"],
        "msg": error["msg"],
        "type": error["type"]
    } for error in errors]

def format_exception(exc: Exception) -> Dict[str, str]:
    """格式化异常信息"""
    return {
        "type": exc.__class__.__name__,
        "message": str(exc),
        "traceback": traceback.format_exc()
    }