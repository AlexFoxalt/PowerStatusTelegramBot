from datetime import datetime

import telegram
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from telegram.ext import ContextTypes

import config.templates as tmpText
from app.logger import get_logger

from app.utils import get_hours_and_mins, ping
from config.base import Config as Cfg
from db.base import DB
from db.models import Light
from db.utils import get_subscribed_users, get_last_light_value

logger = get_logger(__name__)

PREV_LIGHT_VALUE = None


async def run_status_update(context: ContextTypes.DEFAULT_TYPE):
    global PREV_LIGHT_VALUE

    if PREV_LIGHT_VALUE is None:
        PREV_LIGHT_VALUE = await get_last_light_value()

    status = ping(Cfg.ROUTER_IP)
    if PREV_LIGHT_VALUE == status:
        # If no changes were noticed, just pass
        return

    if PREV_LIGHT_VALUE is None:
        async_session = sessionmaker(
            DB, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            session.add(Light(value=not status, mins_from_prev=0))
            await session.commit()
            return

    logger.info(f"Status update {PREV_LIGHT_VALUE} -> {status}")
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(Light.time_created).order_by(Light.time_created.desc())
        result = await session.execute(db_q)
        last_light_status = result.scalars().first()
        mins_from_prev = (
            datetime.utcnow() - last_light_status.replace(tzinfo=None)
        ).seconds // 60
        session.add(Light(value=status, mins_from_prev=mins_from_prev))
        await session.commit()

    PREV_LIGHT_VALUE = status

    formatted_time = get_hours_and_mins(mins_from_prev)
    subscribed_users = await get_subscribed_users()
    logger.info(f"Sending notification for {len(subscribed_users)} users")
    if subscribed_users:
        if status:
            text = (
                f"{tmpText.TMP_LIGHT_NOTIFICATION_ON}\n\n"
                f"{tmpText.TMP_LIGHT_TIME_NOTIFICATION_ON}: {formatted_time}"
            )
        else:
            text = (
                f"{tmpText.TMP_LIGHT_NOTIFICATION_OFF}\n\n"
                f"{tmpText.TMP_LIGHT_TIME_NOTIFICATION_OFF}: {formatted_time}"
            )

        for user_tg_id in subscribed_users:
            await context.bot.send_message(
                chat_id=user_tg_id,
                text=text + tmpText.TMP_NOTIFICATION_REASON,
                parse_mode=telegram.constants.ParseMode.HTML,
            )
