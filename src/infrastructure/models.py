from typing import Optional

from sqlalchemy import BigInteger, DECIMAL, DateTime, Index, Integer, String, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Comment(Base):
    __tablename__ = 'comment'

    comment_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='评论ID')
    user_id: Mapped[int] = mapped_column(BigInteger, comment='评论者ID')
    prompt_id: Mapped[int] = mapped_column(BigInteger, comment='提示词ID')
    content: Mapped[str] = mapped_column(Text(collation='utf8mb4_general_ci'), comment='评论内容')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='创建时间')
    parent_id: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'"), comment='父评论ID')
    like_count: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"), comment='点赞数')


class Favorite(Base):
    __tablename__ = 'favorite'

    favorite_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='收藏ID')
    user_id: Mapped[int] = mapped_column(BigInteger, comment='用户ID')
    prompt_id: Mapped[int] = mapped_column(BigInteger, comment='提示词ID')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='收藏时间')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        Index('order_no', 'order_no', unique=True),
    )

    order_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='订单ID')
    order_no: Mapped[str] = mapped_column(String(32, 'utf8mb4_general_ci'), comment='订单号')
    buyer_id: Mapped[int] = mapped_column(BigInteger, comment='买家ID')
    prompt_id: Mapped[int] = mapped_column(BigInteger, comment='提示词ID')
    amount: Mapped[decimal.Decimal] = mapped_column(DECIMAL(12, 2), comment='支付金额')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='创建时间')
    status: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'0'"), comment='状态（0-待支付 1-已完成 2-已取消）')
    pay_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='支付时间')


class Post(Base):
    __tablename__ = 'post'

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='分类ID')
    name: Mapped[str] = mapped_column(String(20, 'utf8mb4_general_ci'), comment='分类名称')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='创建时间')
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"), comment='父分类ID')
    sort_order: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"), comment='展示排序')


class Prompt(Base):
    __tablename__ = 'prompt'

    prompt_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='提示词ID')
    user_id: Mapped[int] = mapped_column(BigInteger, comment='发布者ID')
    title: Mapped[str] = mapped_column(String(50, 'utf8mb4_general_ci'), comment='标题')
    content: Mapped[str] = mapped_column(Text(collation='utf8mb4_general_ci'), comment='提示词内容')
    category_id: Mapped[int] = mapped_column(Integer, comment='分类ID')
    price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(12, 2), comment='价格')
    prompt_type: Mapped[int] = mapped_column(TINYINT, comment='类型（1-交易 2-竞价 3-文章）')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='创建时间')
    cover: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'), comment='封面图链接')
    view_count: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"), comment='浏览次数')
    status: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'0'"), comment='状态（0-待审核 1-已上架 2-已下架）')
    update_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='更新时间')


class PromptTag(Base):
    __tablename__ = 'prompt_tag'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='关联ID')
    prompt_id: Mapped[int] = mapped_column(BigInteger, comment='提示词ID')
    tag_id: Mapped[int] = mapped_column(BigInteger, comment='标签ID')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='关联时间')


class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = (
        Index('tag_name', 'tag_name', unique=True),
    )

    tag_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='标签ID')
    tag_name: Mapped[str] = mapped_column(String(20, 'utf8mb4_general_ci'), comment='标签名称')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='创建时间')
    use_count: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"), comment='使用次数')


class TestRecord(Base):
    __tablename__ = 'test_record'

    record_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='记录ID')
    user_id: Mapped[int] = mapped_column(BigInteger, comment='测试者ID')
    prompt_id: Mapped[int] = mapped_column(BigInteger, comment='提示词ID')
    input_text: Mapped[str] = mapped_column(Text(collation='utf8mb4_general_ci'), comment='输入文本')
    output_text: Mapped[str] = mapped_column(Text(collation='utf8mb4_general_ci'), comment='输出结果')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='创建时间')
    rating: Mapped[Optional[int]] = mapped_column(TINYINT, comment='评分（1-5）')


class Transaction(Base):
    __tablename__ = 'transaction'

    txn_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='流水ID')
    user_id: Mapped[int] = mapped_column(BigInteger, comment='用户ID')
    amount: Mapped[decimal.Decimal] = mapped_column(DECIMAL(12, 2), comment='变动金额')
    balance: Mapped[decimal.Decimal] = mapped_column(DECIMAL(12, 2), comment='变动后余额')
    txn_type: Mapped[int] = mapped_column(TINYINT, comment='类型（1-充值 2-消费 3-收入）')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='创建时间')
    related_id: Mapped[Optional[str]] = mapped_column(String(32, 'utf8mb4_general_ci'), comment='关联业务ID')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        Index('username', 'username', unique=True),
    )

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment='用户ID')
    username: Mapped[str] = mapped_column(String(50, 'utf8mb4_general_ci'), comment='用户名')
    nickname: Mapped[str] = mapped_column(String(50, 'utf8mb4_general_ci'), comment='用户昵称')
    password: Mapped[str] = mapped_column(String(100, 'utf8mb4_general_ci'), comment='加密密码')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='注册时间')
    avatar: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'), comment='头像URL')
    intro: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_general_ci'), comment='个人简介')
    lex_coin_balance: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(12, 2), server_default=text("'0.00'"), comment='词易币余额')
    status: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text("'0'"), comment='用户状态（0-正常 1-禁用）')
    last_login_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='上次登录时间')