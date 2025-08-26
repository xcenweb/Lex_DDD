from sqlalchemy import select, desc, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PromptTagPublic, PromptTag


class PromptTagService:
    """
    提示词标签服务
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_public_tag_list(self):
        """
        获取公开标签列表，按order排序

        Returns:
            list: 标签列表
        """
        # 查询状态为显示的公开标签，按order排序
        query = select(PromptTagPublic).where(
            PromptTagPublic.status == 1
        ).order_by(
            PromptTagPublic.order.desc(),
            PromptTagPublic.click_count.desc()
        )

        result = await self.db.execute(query)
        tags = result.scalars().all()

        # 转换为字典列表，包含指定字段
        tag_list = [
            {
                "id": tag.real_tag_id,
                "order": tag.order,
                "name": tag.name,
                "click_count": tag.click_count,
                "created_at": tag.created_at.strftime("%Y-%m-%d %H:%M:%S") if tag.created_at else None
            }
            for tag in tags
        ]

        return tag_list

    async def get_tag_list(self, keyword: str = "", page: int = 1, page_size: int = 10):
        """
        获取标签列表，支持关键词搜索和分页

        Args:
            keyword: 搜索关键词
            page: 页码
            page_size: 每页数量

        Returns:
            dict: 包含标签列表和分页信息
        """
        # 计算偏移量
        offset = (page - 1) * page_size

        # 构建查询条件
        conditions = [PromptTag.status == 1]

        # 如果有关键词，添加模糊搜索条件
        if keyword:
            conditions.append(PromptTag.name.like(f"%{keyword}%"))

        # 查询标签，按点击次数和创建时间排序
        query = select(PromptTag).where(
            *conditions
        ).order_by(
            desc(PromptTag.click_count),
            desc(PromptTag.created_at)
        ).offset(offset).limit(page_size)

        result = await self.db.execute(query)
        tags = result.scalars().all()

        # 计算总记录数
        count_query = select(func.count()).select_from(PromptTag).where(*conditions)
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()

        # 计算总页数
        pages = (total + page_size - 1) // page_size

        # 转换为字典列表
        tag_list = [
            {
                "id": tag.id,
                "name": tag.name,
                "click_count": tag.click_count,
                "created_at": tag.created_at.strftime("%Y-%m-%d %H:%M:%S") if tag.created_at else None
            }
            for tag in tags
        ]

        # 返回结果，包含分页信息
        return {
            "items": tag_list,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        }