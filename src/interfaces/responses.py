"""响应处理模块

提供统一的API响应格式处理
"""
from typing import Any, Optional

from fastapi.responses import JSONResponse


def create_response(
    status_code: int = 200,
    message: str = "操作成功",
    data: Optional[Any] = None,
    detail: Optional[Any] = None
) -> JSONResponse:
    """创建统一格式的API响应

    Args:
        status_code: HTTP状态码
        message: 响应消息
        data: 响应数据
        detail: 详细信息（通常用于调试）

    Returns:
        JSONResponse: FastAPI的JSON响应对象
    """
    content = {
        "code": status_code,
        "msg": message,
        "data": data
    }

    if detail is not None:
        content["detail"] = detail

    return JSONResponse(
        status_code=status_code,
        content=content
    )