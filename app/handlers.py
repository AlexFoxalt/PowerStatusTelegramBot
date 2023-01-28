import re
from datetime import datetime, timedelta

import telegram
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import ContextTypes, ConversationHandler

import config.buttons as btnText
import config.templates as tmpText
from app.decorators import admin_only
from app.logger import get_logger
from app.utils import (
    format_time,
    convert_tz,
    get_hours_and_mins,
    get_date_and_month,
    get_percent_of_two,
)
from config.base import Config as Cfg
from db.base import DB
from db.models import User, Base, Light, Message, PinnedMessage
from db.utils import is_registered, get_light_stat, get_users_stat

SELECTED_FLAT, SUPPORT_MSG, SELECTED_HOME, SELECTED_NONE = range(4)
PINNED_MSG = None
logger = get_logger(__name__)


@admin_only
async def migrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with DB.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text="Successfully migrated to fresh DB",
    )
    await DB.dispose()


@admin_only
async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    target_id, message = re.findall(r"/msg (\d*) (.*)", update.message.text)[0]
    await context.bot.send_message(
        chat_id=target_id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=message + tmpText.TMP_NO_REPLY_POSTFIX,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Successfully sent message to {target_id}",
    )


@admin_only
async def msgpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PINNED_MSG

    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    updated_msg = re.findall(r"/msgpin (.*)", update.message.text)[0]
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        session.add(PinnedMessage(text=updated_msg))
        await session.commit()

    PINNED_MSG = updated_msg
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Successfully pinned new message:\n\n{updated_msg}",
    )
    return await menu(update, context)


@admin_only
async def msgall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    message = re.findall(r"/msgall (.*)", update.message.text)[0]
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(User.tg_id)
        result = await session.execute(db_q)
        users = result.scalars().all()
        for user_id in users:
            await context.bot.send_message(
                chat_id=user_id,
                parse_mode=telegram.constants.ParseMode.HTML,
                text=f"{tmpText.TMP_ADMIN_MSG_PREFIX}\n\n"
                f"{message}\n\n"
                f"{tmpText.TMP_NO_REPLY_ALL_POSTFIX}",
            )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Successfully sent messages to {len(users)} users",
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PINNED_MSG

    if PINNED_MSG is None:
        async_session = sessionmaker(
            DB, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            db_q = select(PinnedMessage).order_by(
                PinnedMessage.time_created.desc()
            )
            result = await session.execute(db_q)
            pinned_msg = result.scalars().first()
            if pinned_msg:
                PINNED_MSG = pinned_msg.text
            else:
                PINNED_MSG = Cfg.DEFAULT_PINNED_MSG

    keyboard = [
        [
            InlineKeyboardButton(
                btnText.BTN_MENU_LIGHT, callback_data="light_info"
            )
        ],
        [
            InlineKeyboardButton(
                btnText.BTN_MENU_STAT, callback_data="stat_info"
            )
        ],
        [InlineKeyboardButton(btnText.BTN_MENU_SUB, callback_data="sub_info")],
        [
            InlineKeyboardButton(
                btnText.BTN_USERS_INFO, callback_data="users_info"
            )
        ],
        [
            InlineKeyboardButton(
                btnText.BTN_MENU_SUPPORT, callback_data="support_info"
            )
        ],
        [
            InlineKeyboardButton(
                btnText.BTN_MENU_DTEK, callback_data="dtek_info"
            ),
            InlineKeyboardButton(
                btnText.BTN_MENU_INFO, callback_data="bot_info"
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{tmpText.TMP_MENU}\n\n📌 <i>{PINNED_MSG}</i>",
        reply_markup=reply_markup,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    possibles = globals().copy()
    possibles.update(locals())
    return await possibles.get(query.data)(update, context)


async def light_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(Light).order_by(Light.time_created.desc())
        result = await session.execute(db_q)
        light = result.scalars().first()

    time_passed = (
        datetime.utcnow() - light.time_created.replace(tzinfo=None)
    ).seconds // 60
    time_passed = get_hours_and_mins(time_passed)
    light.time_created = convert_tz(light.time_created)

    if light.value:
        text = tmpText.TMP_LIGHT_ON
    else:
        text = tmpText.TMP_LIGHT_OFF

    text = text.format(
        time_of_event=format_time(light.time_created), time_passed=time_passed
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=text,
    )
    return ConversationHandler.END


async def sub_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    user_status_mapping = {
        True: tmpText.TMP_USER_SUBED,
        False: tmpText.TMP_USER_UNSUBED,
    }
    button_status_mapping = {
        False: [
            InlineKeyboardButton(btnText.BTN_SUB_ME, callback_data="sub_me")
        ],
        True: [
            InlineKeyboardButton(
                btnText.BTN_UNSUB_ME, callback_data="unsub_me"
            )
        ],
    }
    query = update.callback_query

    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(User).where(User.tg_id == query.from_user["id"])
        result = await session.execute(db_q)
        user_sub_status = result.scalars().first().news_subscribed

    keyboard = [button_status_mapping[user_sub_status]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{user_status_mapping[user_sub_status]}",
        reply_markup=reply_markup,
        parse_mode=telegram.constants.ParseMode.HTML,
    )
    return ConversationHandler.END


async def sub_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    query = update.callback_query
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(User).where(User.tg_id == query.from_user["id"])
        result = await session.execute(db_q)
        user = result.scalars().first()
        if not user.news_subscribed:
            user.news_subscribed = True
            await session.commit()
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=tmpText.TMP_SUB_SUCCESS
            )
    return ConversationHandler.END


async def unsub_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    query = update.callback_query
    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        db_q = select(User).where(User.tg_id == query.from_user["id"])
        result = await session.execute(db_q)
        user = result.scalars().first()
        if user.news_subscribed:
            user.news_subscribed = False
            await session.commit()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=tmpText.TMP_UNSUB_SUCCESS,
            )
    return ConversationHandler.END


async def users_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    users_stat = await get_users_stat()
    total_users = sum(users_stat.values())
    percentage_text = []
    for home, user_count in users_stat.items():
        percent = round(user_count * 100 / total_users)
        if home is None:
            percentage_text.append(
                tmpText.TMP_USER_INFO_HOME_PERCENT.format(
                    home="\n🥸 Анонимы", percent=percent
                )
            )
        else:
            percentage_text.append(
                tmpText.TMP_USER_INFO_HOME_PERCENT.format(
                    home=f"🛖 Дом {home}", percent=percent
                )
            )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=tmpText.TMP_USER_INFO.format(total_reg=total_users)
        + "\n".join(sorted(percentage_text, reverse=True)),
    )
    return ConversationHandler.END


async def dtek_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        photo=Cfg.get_dtek_media(),
        caption=tmpText.TMP_DTEK_INFO,
    )
    return ConversationHandler.END


async def support_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
    ]
    await context.bot.send_message(
        reply_markup=InlineKeyboardMarkup(keyboard),
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=tmpText.TMP_SUPPORT_INFO,
    )
    return SUPPORT_MSG


async def bot_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=tmpText.TMP_BOT_INFO,
    )
    return ConversationHandler.END


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    await menu(update, context)
    return ConversationHandler.END


async def stat_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.effective_chat.username}({update.effective_chat.id})"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=tmpText.TMP_STAT_INFO_MAIN,
    )

    now = datetime.utcnow().date()
    week_ago = now - timedelta(days=6)
    week_stat = await get_light_stat(week_ago, now)
    text = tmpText.TMP_STAT_INFO_LAST_WEEK.format(
        stat_date_week_ago=get_date_and_month(week_ago),
        stat_date_now=get_date_and_month(now),
        light_off_time=get_hours_and_mins(week_stat["light_off_mins"]),
        light_on_time=get_hours_and_mins(week_stat["light_on_mins"]),
        light_turn_on_avg_data=get_hours_and_mins(
            round(week_stat["light_turn_on_avg_data"])
        ),
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=text,
    )

    now = now - timedelta(days=1)
    week_ago = now - timedelta(days=6)
    two_weeks_ago = now - timedelta(days=12)
    two_weeks_stat = await get_light_stat(two_weeks_ago, week_ago)

    if not all(two_weeks_stat.values()):
        # Not enough data
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode=telegram.constants.ParseMode.HTML,
            text=tmpText.TMP_STAT_INFO_NO_DATA.format(
                stat_date_week_ago=get_date_and_month(two_weeks_ago),
                stat_date_now=get_date_and_month(week_ago),
            ),
        )
        return ConversationHandler.END

    text = tmpText.TMP_STAT_INFO_LAST_TWO_WEEKS.format(
        stat_date_week_ago=get_date_and_month(two_weeks_ago),
        stat_date_now=get_date_and_month(week_ago),
        light_off_time=get_hours_and_mins(two_weeks_stat["light_off_mins"]),
        light_on_time=get_hours_and_mins(two_weeks_stat["light_on_mins"]),
        light_turn_on_avg_data=get_hours_and_mins(
            round(two_weeks_stat["light_turn_on_avg_data"])
        ),
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=text,
    )

    compare_light_on_data = get_percent_of_two(
        week_stat["light_on_mins"], two_weeks_stat["light_on_mins"]
    )
    compare_light_on_avg_time = get_percent_of_two(
        week_stat["light_turn_on_avg_data"],
        two_weeks_stat["light_turn_on_avg_data"],
    )

    if compare_light_on_data < 0:
        less_or_more = "меньше на "
        emoji = btnText.BTN_STAT_LESS
    elif compare_light_on_data > 0:
        less_or_more = "больше на +"
        emoji = btnText.BTN_STAT_MORE
    else:
        # Division zero
        return

    if compare_light_on_avg_time < 0:
        less_or_more_avg = "меньше на "
        emoji_avg = btnText.BTN_STAT_LESS
    elif compare_light_on_avg_time > 0:
        less_or_more_avg = "больше на +"
        emoji_avg = btnText.BTN_STAT_MORE
    else:
        less_or_more_avg = "не менялось"
        emoji_avg = btnText.BTN_STAT_EQUAL

    text = tmpText.TMP_STAT_INFO_COMPARE.format(
        light_on_time=compare_light_on_data,
        emoji=emoji,
        less_or_more=less_or_more,
        light_on_time_avg=compare_light_on_avg_time,
        emoji_avg=emoji_avg,
        less_or_more_avg=less_or_more_avg,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=text,
    )
    return ConversationHandler.END


async def register_support_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    logger.info(
        f"{update.message.from_user.username}({update.message.from_user.id})"
    )
    user = update.message.from_user.id
    text = update.message.text

    if text == "/start":
        return await back_to_menu(update, context)

    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        session.add(Message(message=text, user_id=user))
        await session.commit()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=tmpText.TMP_SUPPORT_MSG_CREATED,
    )

    await context.bot.send_message(
        chat_id=Cfg.ADMIN_ID,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=f"🆘 <b>New message to support</b>\n"
        f"From: {user}\n"
        f"Msg: {text}",
    )
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.message.from_user.username}({update.message.from_user.id})"
    )
    if await is_registered(update.message.from_user.id):
        return await menu(update, context)
    else:
        return await register_step_one(update, context)


async def register_step_one(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    logger.info(
        f"{update.message.from_user.username}({update.message.from_user.id})"
    )
    reply_keyboard = [
        [
            btnText.BTN_SELECT_HOME_B,
            btnText.BTN_SELECT_HOME_V,
            btnText.BTN_SELECT_HOME_G,
        ],
        [btnText.BTN_SKIP],
    ]
    await update.message.reply_text(
        tmpText.TMP_REGISTER_STEP_ONE,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Адрес дома",
            resize_keyboard=True,
        ),
    )
    return SELECTED_HOME


async def register_step_two(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    logger.info(
        f"{update.message.from_user.username}({update.message.from_user.id})"
    )
    if update.message.text == btnText.BTN_SKIP:
        return await register_end(update, context)

    context.user_data["home"] = update.message.text
    reply_keyboard = [[btnText.BTN_SKIP]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=tmpText.TMP_REGISTER_FLAT_NUM,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Номер квартиры",
        ),
        parse_mode=telegram.constants.ParseMode.HTML,
    )
    return SELECTED_FLAT


async def register_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"{update.message.from_user.username}({update.message.from_user.id})"
    )
    if update.message.text == btnText.BTN_SKIP:
        flat = None
    else:
        flat = int(update.message.text)
    user = update.message.from_user

    async_session = sessionmaker(
        DB, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        session.add(
            User(
                tg_id=user.id,
                username=user.username,
                home=context.user_data.get("home"),
                flat=flat,
            )
        )
        await session.commit()
    await DB.dispose()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=tmpText.TMP_REGISTER_SUCCESS,
        reply_markup=ReplyKeyboardRemove(),
    )
    await context.bot.send_message(
        chat_id=Cfg.ADMIN_ID,
        text=f"✴ <b>New registration</b>\n\n"
        f"ID: {user.id}\n"
        f"Username: {user.username}\n"
        f'Home: {context.user_data.get("home")}\n'
        f"Flat: {flat}",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=telegram.constants.ParseMode.HTML,
    )
    return await start(update, context)
