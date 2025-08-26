from fastapi import APIRouter, Request, Query, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.responses import create_response

from app.services.prompt.tag import PromptTagService
from app.services.prompt.recommend import PromptRecommendService
from app.services.prompt.content import PromptContentService

router = APIRouter(prefix="/prompt", tags=["prompt recommend"])

class RecommendPrompt(BaseModel):
    page: int = Query(default=1, ge=1, description="页码")
    page_size: int = Query(default=15, ge=15, le=15, description="每页数量")
    tag_id: int = Query(default=0, description="标签ID，0表示全部")

@router.get("/public/tag", summary="首页公开标签列表")
async def get_tag_list(request: Request, db: AsyncSession = Depends(get_db)):
    # 调用标签服务获取公开标签列表
    tag_service = PromptTagService(db)
    tag_list = await tag_service.get_public_tag_list()
    return create_response(data=tag_list)


@router.get("/recommend", summary="推荐的提示词列表")
async def get_prompt_list(
    request: Request,
    tag_id: int = Query(default=0, description="标签ID，0表示全部"),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=15, ge=15, le=15, description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    # 调用推荐服务获取推荐提示词列表
    recommend_service = PromptRecommendService(db)
    result = await recommend_service.get_recommend_prompts(page, page_size, tag_id)
    return create_response(data=result)


@router.get("/content", summary="获取提示词内容")
async def get_prompt_content(
    request: Request,
    prompt_id: int = Query(description="提示词ID"),
    db: AsyncSession = Depends(get_db)
):
    # 调用提示词内容服务获取内容
    content_service = PromptContentService(db)
    result = await content_service.get_prompt_content(prompt_id, 6)
    return create_response(data=result)