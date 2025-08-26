from sqlalchemy import select, update, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Prompts, Users, UserViewPrompts


class PromptContentService:
    """提示词内容服务"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_prompt_content(self, prompt_id: int, user_id: int = None) -> dict:
        """获取提示词内容

        Args:
            prompt_id: 提示词ID
            user_id: 用户ID，可选

        Returns:
            dict: 提示词内容信息
        """
        # 查询提示词基本信息
        prompt_query = select(Prompts).where(
            Prompts.id == prompt_id,
            Prompts.status == 1,
            Prompts.is_deleted == 0
        )
        prompt_result = await self.db.execute(prompt_query)
        prompt = prompt_result.scalar_one_or_none()

        if not prompt:
            return {}

        # 更新浏览量
        update_query = update(Prompts).where(
            Prompts.id == prompt_id
        ).values(
            view_count=Prompts.view_count + 1
        )
        await self.db.execute(update_query)

        # 如果提供了用户ID，记录用户浏览记录
        if user_id:
            # 查询是否存在浏览记录
            view_query = select(UserViewPrompts).where(
                UserViewPrompts.user_id == user_id,
                UserViewPrompts.prompt_id == prompt_id
            )
            view_result = await self.db.execute(view_query)
            view_record = view_result.scalar_one_or_none()

            if view_record:
                # 更新浏览时间
                update_view_query = update(UserViewPrompts).where(
                    UserViewPrompts.user_id == user_id,
                    UserViewPrompts.prompt_id == prompt_id
                ).values(view_at=func.current_timestamp())
                await self.db.execute(update_view_query)
            else:
                # 创建新的浏览记录
                insert_view_query = insert(UserViewPrompts).values(
                    user_id=user_id,
                    prompt_id=prompt_id
                )
                await self.db.execute(insert_view_query)

        await self.db.commit()

        # 查询作者信息
        user_query = select(Users).where(
            Users.id == prompt.user_id,
            Users.status == 1,
            Users.is_deleted == 0
        )
        user_result = await self.db.execute(user_query)
        user = user_result.scalar_one_or_none()

        # 从tag_cache获取标签信息
        tags = []
        if prompt.tag_cache:
            tag_names = prompt.tag_cache.split(',')
            tags = [name.strip() for name in tag_names]

        # 组装返回数据
        return {
            "id": prompt.id,
            "type": prompt.type,

            "images": eval(prompt.images) if prompt.images else [],
            "title": prompt.title,
            "tags": tags,
            "content": eval(prompt.content),

            "counts": {
                "comment": prompt.comment_count,
                "view": prompt.view_count + 1,
                "like": prompt.like_count,
                "favorite": prompt.favorite_count,
            },

            "author": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else None,
                "avatar_url": user.avatar_url if user else None,
                "bio": user.bio if user else None,
                "relation": {
                    "is_followed": False, # TODO
                }
            },

            "is_liked": False, # TODO
            "is_favorited": False, # TODO
            "created_at": str(prompt.created_at),
            "updated_at": str(prompt.updated_at),
        }