from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from db.models import User, Light
from db.base import DB


async def is_registered(tg_id: int) -> bool:
    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        db_q = select(User).where(User.tg_id == tg_id)
        result = await session.execute(db_q)
        user = result.scalars().first()
    return bool(user)


async def get_subscribed_users() -> list:
    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        db_q = select(User.tg_id).where(User.news_subscribed.is_(True))
        result = await session.execute(db_q)
        return result.scalars().all()


async def get_last_light_value() -> bool:
    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        db_q = select(Light.value).order_by(Light.time_created.desc())
        result = await session.execute(db_q)
        return result.scalars().first()
