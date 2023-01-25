import datetime

from cache import AsyncTTL
from sqlalchemy import and_, func, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import count

from app.logger import get_logger
from db.base import DB
from db.models import User, Light

logger = get_logger(__name__)


async def is_registered(tg_id: int) -> bool:
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(User).where(User.tg_id == tg_id)
        result = await session.execute(db_q)
        user = result.scalars().first()
    return bool(user)


async def get_subscribed_users() -> list:
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(User.tg_id).where(User.news_subscribed.is_(True))
        result = await session.execute(db_q)
        return result.scalars().all()


async def get_last_light_value() -> bool:
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(Light.value).order_by(Light.time_created.desc())
        result = await session.execute(db_q)
        return result.scalars().first()


@AsyncTTL(time_to_live=60 * 60, maxsize=4)  # ttl = 1 hour
async def get_light_stat(start: datetime, stop: datetime) -> dict:
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(func.sum(Light.mins_from_prev)).filter(
            and_(
                Light.time_created >= start,
                cast(Light.time_created, Date) <= stop,
                Light.value == False,  # noqa:
            )
        )
        result = await session.execute(db_q)
        light_turn_on_data = result.scalars().first()

        db_q = select(func.sum(Light.mins_from_prev)).filter(
            and_(
                Light.time_created >= start,
                cast(Light.time_created, Date) <= stop,
                Light.value == True,  # noqa:
            )
        )
        result = await session.execute(db_q)
        light_turn_off_data = result.scalars().first()

        db_q = select(func.avg(Light.mins_from_prev)).filter(
            and_(
                Light.time_created >= start,
                cast(Light.time_created, Date) <= stop,
                Light.value == False,  # noqa:
            )
        )
        result = await session.execute(db_q)
        light_turn_on_avg_data = result.scalars().first()

    return {
        "light_on_mins": light_turn_on_data
        if light_turn_on_data is not None
        else 0,
        "light_off_mins": light_turn_off_data
        if light_turn_on_data is not None
        else 0,
        "light_turn_on_avg_data": light_turn_on_avg_data
        if light_turn_on_avg_data is not None
        else 0,
    }


@AsyncTTL(time_to_live=60 * 60, maxsize=1)
async def get_users_stat() -> dict:
    response = {}
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(User.home, count(User.id)).group_by(User.home)
        result = await session.execute(db_q)
        for row in result:
            response[row[0]] = row[1]
        return response
