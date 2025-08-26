from typing import Optional

from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, ENUM, INTEGER, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass


class AppVersion(Base):
    __tablename__ = 'app_version'
    __table_args__ = (
        Index('uk_version_platform', 'version', 'platform', unique=True),
        {'comment': '记录版本'}
    )

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='发布时间')
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    version: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'), comment='版本号')
    platform: Mapped[Optional[str]] = mapped_column(ENUM('android', 'ios', 'pc'), server_default=text("'android'"), comment='平台')
    url: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='下载链接（限安卓）')
    desc: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'), comment='更新简介')


class PromptComments(Base):
    __tablename__ = 'prompt_comments'
    __table_args__ = (
        Index('idx_comment_tree', 'prompt_id', 'root_id', 'parent_id'),
        Index('idx_prompt_created_time', 'prompt_id', 'created_at'),
        Index('idx_prompt_root_parent', 'prompt_id', 'root_id', 'parent_id'),
        Index('idx_user_comments', 'user_id', 'created_at'),
        {'comment': '提示词评论表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(BIGINT, server_default=text("'0'"), comment='评论者id')
    prompt_id: Mapped[Optional[int]] = mapped_column(BIGINT, server_default=text("'0'"), comment='文章id')
    root_id: Mapped[Optional[int]] = mapped_column(BIGINT, server_default=text("'0'"), comment='根评论id')
    parent_id: Mapped[Optional[int]] = mapped_column(BIGINT, server_default=text("'0'"), comment='父评论id')
    content: Mapped[Optional[str]] = mapped_column(VARCHAR(200), comment='评论内容')
    likes_count: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='点赞数')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='评论时间')
    is_deleted: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'0'"), comment='0-正常 1-删除')


class PromptSearchRecords(Base):
    __tablename__ = 'prompt_search_records'
    __table_args__ = {'comment': '提示词搜索关键词记录'}

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    keyword: Mapped[str] = mapped_column(String(50, 'utf8mb4_general_ci'), comment='被搜索关键词')
    search_count: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'"), comment='被搜索次数')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='第一次被搜索时间')
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后一次被搜索时间')
    status: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'1'"), comment='1-显示 2-隐藏')


class PromptTag(Base):
    __tablename__ = 'prompt_tag'
    __table_args__ = (
        Index('uk_name', 'name', unique=True),
        {'comment': '全部标签表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='标签ID')
    name: Mapped[str] = mapped_column(VARCHAR(50), comment='标签名')
    click_count: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'"), comment='访问、点击次数')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    status: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'1'"), comment='0-禁用 1-显示')


class PromptTagPublic(Base):
    __tablename__ = 'prompt_tag_public'
    __table_args__ = (
        Index('uk_name', 'name', unique=True),
        {'comment': '公开标签表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='标签ID')
    real_tag_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='对应的标签真实id')
    order: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'0'"), comment='排序')
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(50), comment='公开标签名')
    click_count: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'"), comment='点击次数')
    status: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'1'"), comment='0-隐藏 1-显示')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class PromptTagRelation(Base):
    __tablename__ = 'prompt_tag_relation'
    __table_args__ = (
        Index('idx_tag_id', 'tag_id'),
        {'comment': '提示词标签关联表'}
    )

    prompt_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='文章ID')
    tag_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='标签ID')


class Prompts(Base):
    __tablename__ = 'prompts'
    __table_args__ = (
        Index('ft_content_search', 'title', 'summary_content', 'content'),
        Index('idx_user_id', 'user_id'),
        {'comment': '提示词文章表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='文章ID')
    user_id: Mapped[int] = mapped_column(BIGINT, comment='发布者ID')
    title: Mapped[str] = mapped_column(VARCHAR(15), comment='标题')
    tag_cache: Mapped[str] = mapped_column(TEXT, comment='该提示词的标签缓存')
    summary_content: Mapped[str] = mapped_column(VARCHAR(40), comment='根据content解析生成的摘要内容')
    content: Mapped[str] = mapped_column(TEXT, comment='内容')
    type: Mapped[Optional[str]] = mapped_column(ENUM('article', 'vending', 'auction'), server_default=text("'article'"), comment='图文、售卖、拍卖')
    cover_image: Mapped[Optional[str]] = mapped_column(TEXT, comment='封面图URL')
    images: Mapped[Optional[str]] = mapped_column(TEXT, comment='所有图片URL')
    like_count: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='点赞数')
    comment_count: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='评论数')
    favorite_count: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='收藏数')
    view_count: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='查看数')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='更新时间')
    status: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'1'"), comment='0-草稿  1-已发布 2-待审核')
    is_deleted: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'0'"), comment='0-正常 1-删除')


class UserChat(Base):
    __tablename__ = 'user_chat'
    __table_args__ = (
        Index('idx_conversation', 'sender_id', 'receiver_id', 'created_at'),
        Index('idx_receiver_sender_time', 'receiver_id', 'sender_id', 'created_at'),
        {'comment': '聊天私信表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    sender_id: Mapped[int] = mapped_column(BIGINT, comment='发送者id')
    receiver_id: Mapped[int] = mapped_column(BIGINT, comment='接收者id')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    content: Mapped[Optional[str]] = mapped_column(TEXT, comment='消息内容')
    is_read: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"), comment='1-已读 0-未读')


class UserExpRecords(Base):
    __tablename__ = 'user_exp_records'
    __table_args__ = (
        Index('idx_exp_flow', 'user_id', 'created_at'),
        Index('idx_user_time', 'user_id', 'created_at'),
        {'comment': '用户经验值变化记录表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='记录ID')
    user_id: Mapped[int] = mapped_column(BIGINT, comment='用户ID')
    exp_change: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"), comment='经验变化值')
    reason: Mapped[Optional[str]] = mapped_column(VARCHAR(50), comment='变化原因')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))


class UserFavoriteFolders(Base):
    __tablename__ = 'user_favorite_folders'
    __table_args__ = (
        Index('idx_folder_visibility', 'user_id', 'visibility'),
        {'comment': '用户的收藏夹'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, comment='用户id')
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(50), server_default=text("'默认收藏夹'"), comment='收藏夹名称')
    desc: Mapped[Optional[str]] = mapped_column(TEXT, comment='收藏夹描述')
    sort_order: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'0'"), comment='收藏夹排序')
    visibility: Mapped[Optional[str]] = mapped_column(ENUM('private', 'public'), server_default=text("'private'"), comment='是否公开')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class UserFavoritePrompts(Base):
    __tablename__ = 'user_favorite_prompts'
    __table_args__ = (
        Index('idx_prompt_id', 'prompt_id'),
        {'comment': '用户收藏表'}
    )

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='用户id')
    prompt_id: Mapped[int] = mapped_column(BIGINT, comment='文章id')
    folder_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment='收藏夹id')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    is_deleted: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'0'"), comment='0-正常 1-删除')


t_user_follows = Table(
    'user_follows', Base.metadata,
    Column('follower_id', BIGINT, nullable=False, comment='关注者ID'),
    Column('following_id', BIGINT, nullable=False, comment='被关注者ID'),
    Column('created_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间'),
    Column('is_deleted', TINYINT, server_default=text("'0'"), comment='0-正常 1-删除'),
    Index('idx_following_created', 'following_id', 'created_at'),
    Index('idx_following_id', 'following_id'),
    comment='用户关注表'
)


class UserLikes(Base):
    __tablename__ = 'user_likes'
    __table_args__ = (
        Index('idx_like_activity', 'target_type', 'target_id', 'created_at'),
        Index('idx_target', 'target_id', 'target_type'),
        Index('idx_target_type', 'target_type', 'target_id'),
        {'comment': '用户点赞表'}
    )

    target_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='目标ID')
    user_id: Mapped[int] = mapped_column(BIGINT, comment='用户ID')
    target_type: Mapped[Optional[str]] = mapped_column(ENUM('prompt', 'comment'), comment='目标类型')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    is_deleted: Mapped[Optional[int]] = mapped_column(TINYINT, comment='1-删除 0-正常')


class UserPointRecords(Base):
    __tablename__ = 'user_point_records'
    __table_args__ = (
        Index('idx_user_time', 'user_id', 'created_at'),
        {'comment': '积分变化记录表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='记录ID')
    user_id: Mapped[int] = mapped_column(BIGINT, comment='用户ID')
    points_change: Mapped[int] = mapped_column(Integer, server_default=text("'0'"), comment='积分变化值')
    balance: Mapped[int] = mapped_column(BIGINT, server_default=text("'0'"), comment='变化后的积分余额')
    reason: Mapped[Optional[str]] = mapped_column(VARCHAR(50), comment='变化原因')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class UserSigninRecords(Base):
    __tablename__ = 'user_signin_records'
    __table_args__ = (
        Index('idx_signin_continuity', 'user_id', 'signin_at'),
        Index('idx_user_continuous', 'user_id'),
        Index('uk_user_date', 'user_id', unique=True),
        {'comment': '用户每日签到记录表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='记录ID')
    user_id: Mapped[int] = mapped_column(BIGINT, comment='用户ID')
    signin_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class UserTokens(Base):
    __tablename__ = 'user_tokens'
    __table_args__ = (
        Index('idx_user_expires', 'user_id', 'access_expires_at'),
        Index('uk_token', 'access_token', unique=True),
        {'comment': '用户登录令牌表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='令牌ID')
    user_id: Mapped[int] = mapped_column(BIGINT, comment='用户ID')
    ipv4: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='登录时的ipv4')
    ipv6: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='登录时的ipv6')
    device_info: Mapped[Optional[str]] = mapped_column(TEXT, comment='UA设备信息')
    access_token: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='登录令牌')
    refresh_token: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='刷新登录状态令牌')
    access_expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, comment='登录令牌过期时间')
    refresh_expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, comment='刷新令牌过期时间')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class UserViewPrompts(Base):
    __tablename__ = 'user_view_prompts'
    __table_args__ = (
        Index('idx_prompt_id', 'prompt_id'),
        {'comment': '用户浏览提示词记录表'}
    )

    prompt_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='提示词ID')
    user_id: Mapped[int] = mapped_column(BIGINT, comment='用户ID')
    view_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='浏览时间')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('uk_email', 'email', unique=True),
        Index('uk_phone', 'phone', unique=True),
        {'comment': '用户表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='用户ID')
    nickname: Mapped[str] = mapped_column(VARCHAR(50), comment='昵称')
    password: Mapped[str] = mapped_column(VARCHAR(255), comment='哈希后的密码')
    avatar_url: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='头像URL')
    bio: Mapped[Optional[str]] = mapped_column(TEXT, comment='个人简介')
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='邮箱')
    phone_country: Mapped[Optional[int]] = mapped_column(TINYINT, comment='手机号国家代码')
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(20), comment='手机号')
    points: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='积分')
    level: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='等级（0-6级）')
    level_exp: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='当前经验值')
    favorites_count: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='收藏数量')
    follow_count: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='关注数量')
    fans_count: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='粉丝数量')
    prompt_count: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text("'0'"), comment='发布提示词数')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='注册时间')
    last_login_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, comment='最后登录时间')
    status: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'1'"), comment='0-封禁 1-正常')
    is_deleted: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'0'"), comment='0-正常 1-删除')


class VerificationCodes(Base):
    __tablename__ = 'verification_codes'
    __table_args__ = (
        Index('idx_code_validation', 'target', 'type', 'expired_at'),
        Index('idx_expired', 'expired_at'),
        Index('idx_target_type_expired', 'target', 'type', 'expired_at', 'is_used'),
        {'comment': '验证码表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='验证码ID')
    target: Mapped[str] = mapped_column(VARCHAR(100), comment='手机号或邮箱地址')
    type: Mapped[int] = mapped_column(TINYINT, comment='1-手机验证码 2-邮箱验证码')
    code: Mapped[str] = mapped_column(CHAR(6), comment='验证码')
    expired_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, comment='过期时间')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    is_used: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"), comment='是否已使用')
