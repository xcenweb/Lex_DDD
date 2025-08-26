from fastapi import APIRouter, Request, Query
from pydantic import BaseModel

from app.core.responses import create_response

router = APIRouter(prefix="/user", tags=["user social"])

class Follow(BaseModel):
    userid: int = Query(description="目标用户id")
    action: str = Query(description="关注或取关", enum=["follow", "unfollow"])


@router.get("/info/{userid}", summary="获取指定用户的可公开信息")
async def get_userinfo(request: Request, userid: int):
    return create_response()


@router.post("/follow", summary="关注或取关指定用户")
async def follow_user(request: Request, data: Follow):

    return create_response()


@router.get("/fans/list", summary="获取粉丝列表")
async def get_follow_list(request: Request):
    return create_response()