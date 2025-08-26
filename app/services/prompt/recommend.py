from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Prompts, Users, PromptTagPublic, PromptTagRelation


class PromptRecommendService:
    """
    提示词推荐服务
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_post_userinfo(self, prompts: list) -> dict:
        """
        获取提示词关联的用户信息

        Args:
            prompts: 提示词列表

        Returns:
            dict: 用户信息字典，key为用户ID，value为用户对象
        """
        user_ids = [prompt.user_id for prompt in prompts]
        user_query = select(Users).where(
            Users.id.in_(user_ids),
            Users.status == 1,
            Users.is_deleted == 0
        )
        user_result = await self.db.execute(user_query)
        return {user.id: user for user in user_result.scalars().all()}

    async def get_recommend_prompts(self, page: int = 1, page_size: int = 15, tag_id: int = 0):
        """
        获取推荐的提示词列表

        Args:
            db: 数据库会话
            page: 页码
            page_size: 每页数量
            tag_id: 标签ID

        Returns:
            dict: 包含提示词列表和分页信息
        """
        # 计算偏移量
        offset = (page - 1) * page_size

        # 构建基础查询
        query = select(Prompts).where(
            Prompts.status == 1,
            Prompts.is_deleted == 0
        )

        if tag_id != 0:
            # 按标签过滤，并按浏览量和创建时间排序
            query = query.join(
                PromptTagRelation,
                (PromptTagRelation.prompt_id == Prompts.id) & (PromptTagRelation.tag_id == tag_id)
            ).order_by(desc(Prompts.view_count), desc(Prompts.created_at)).offset(offset).limit(page_size)
        else:
            # 按浏览量和创建时间排序
            query = query.order_by(desc(Prompts.view_count), desc(Prompts.created_at)).offset(offset).limit(page_size)

        result = await self.db.execute(query)
        prompts = result.scalars().all()

        # 获取提示词关联的用户信息
        users = await self.get_post_userinfo(prompts)

        # 转换为字典列表，包含提示词信息和用户信息
        prompt_list = []
        for prompt in prompts:
            user = users.get(prompt.user_id)
            prompt_dict = {
                "id": prompt.id,
                "type": prompt.type,

                "cover_image": prompt.cover_image,
                "title": prompt.title,
                "summary_content": prompt.summary_content,

                "like_count": prompt.like_count,
                "view_count": prompt.view_count,

                "author": {
                    "id": prompt.user_id,
                    "nickname": user.nickname if user else None,
                    "avatar_url": user.avatar_url if user else None,
                },
            }
            prompt_list.append(prompt_dict)

        return prompt_list