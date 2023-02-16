from datetime import datetime, time

import telegram
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from telegram.ext import ContextTypes

from config.templates import TEMPLATE
from app.logger import get_logger

from app.utils import get_hours_and_mins, ping, is_time_between
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
        # Previous light value can be still None, if there is no data in db
        # In this case just create plug item
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
        ).total_seconds() // 60
        session.add(Light(value=status, mins_from_prev=int(mins_from_prev)))
        await session.commit()

    PREV_LIGHT_VALUE = status

    disable_sound = is_time_between(
        time(Cfg.DISABLE_SOUND_START_TIME), time(Cfg.DISABLE_SOUND_END_TIME)
    )
    formatted_time = get_hours_and_mins(int(mins_from_prev))
    subscribed_users = await get_subscribed_users()
    logger.info(
        f"Sending notification for {len(subscribed_users)} users | "
        f"No sound: {disable_sound}"
    )
    if subscribed_users:
        if status:
            text = (
                f"{TEMPLATE.TMP_LIGHT_NOTIFICATION_ON}\n\n"
                f"{TEMPLATE.TMP_LIGHT_TIME_NOTIFICATION_ON}: {formatted_time}"
            )
        else:
            text = (
                f"{TEMPLATE.TMP_LIGHT_NOTIFICATION_OFF}\n\n"
                f"{TEMPLATE.TMP_LIGHT_TIME_NOTIFICATION_OFF}: {formatted_time}"
            )

        for user_tg_id in subscribed_users:
            try:
                await context.bot.send_message(
                    chat_id=user_tg_id,
                    text=text + TEMPLATE.TMP_NOTIFICATION_REASON,
                    parse_mode=telegram.constants.ParseMode.HTML,
                    disable_notification=disable_sound,
                )
            except telegram.error.Forbidden as exc:
                logger.warning(f"Exception: {str(exc)} | {user_tg_id}")
