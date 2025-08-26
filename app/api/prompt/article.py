from fastapi import APIRouter, Request, Query, Depends
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.responses import create_response

from app.services.prompt.tag import PromptTagService


router = APIRouter(prefix="/prompt", tags=["prompt article"])

class PromptArticle(BaseModel):
    images: list = Query([], description="图片列表")
    title: str = Query("", description="标题")
    content: str = Query("", description="内容")
    tags: list = Query([], description="标签列表")
    is_draft: bool = Query(True, description="是否保存为草稿")

class UpdatePromptArticle(BaseModel):
    id: int = Query(0, description="文章id。带id为修改文章，不带id为新增文章")
    images: list = Query([], description="图片列表")
    title: str = Query("", description="标题")
    content: str = Query("", description="内容")
    tags: list = Query([], description="标签列表")
    is_draft: bool = Query(True, description="是否保存为草稿")


@router.get("/tag/list", summary="获取可选标签列表")
async def tag_list(
    request: Request,
    keyword: str = Query("", description="搜索关键词"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(default=10, e=10, le=10, description="每页数量"),
    db: AsyncSession = Depends(get_db),
):
    """获取和搜索平台标签列表"""
    # 调用标签服务获取标签列表
    tag_service = PromptTagService(db)
    result = await tag_service.get_tag_list(keyword, page, page_size)
    return create_response(data=result)


@router.post("/article/add", summary="发布提示词文章")
async def add_article(request: Request, data: PromptArticle, db: AsyncSession = Depends(get_db),
):
    """添加文章"""
    return create_response()


@router.post("/article/update", summary="更新提示词文章")
async def update_article(request: Request, data: UpdatePromptArticle, db: AsyncSession = Depends(get_db),
):
    """更新文章"""
    return create_response()