from fastapi import APIRouter, Request, Query
from pydantic import BaseModel

from app.core.db import get_db
from app.core.responses import create_response

router = APIRouter(prefix="/prompt", tags=["prompt search"])

class SearchPrompt(BaseModel):
    keyword: str
    page: int = Query(1, description="页码")
    page_size: int = Query(le=10, description="每页数量")


@router.post("/search", summary="搜索提示词")
async def search_prompt(request: Request, data: SearchPrompt):
    return []


@router.get("/search/hotkey", summary="获取热门搜索关键词排行榜")
async def search_prompt_hotkey(request: Request):
    return []