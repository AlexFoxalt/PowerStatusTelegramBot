import pdb
from datetime import datetime
import re
import telegram
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
)

from app.decorators import admin_only
from app.logger import logger
from app.tasks import ping
from app.utils import format_time, convert_tz
from config.base import Config as Cfg
from config.consts import INFO_TEXT, REG_TEXT, SUPPORT_TEXT
from db.base import DB
from db.models import User, Base, Light, Message
from db.utils import is_registered, get_subscribed_users, get_last_light_value

SELECTED_FLAT, SUPPORT_MSG, SELECTED_HOME, SELECTED_NONE = range(4)
PREV_LIGHT_VALUE = None


@admin_only
async def migrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with DB.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await DB.dispose()


@admin_only
async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_id, message = re.findall(r"/msg (\d*) (.*)", update.message.text)[0]
    await context.bot.send_message(
        chat_id=target_id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=message
        + "\n\n<i>*на это сообщение отвечать не нужно, оно нигде не сохранится</i>",
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Successfully sent message to {target_id}",
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"💡 Свет 💡", callback_data="light_info")],
        [InlineKeyboardButton(f"📊 Статистика 📊", callback_data="stat_info")],
        [InlineKeyboardButton(f"📳 Уведомления 📳", callback_data="sub_info")],
        [InlineKeyboardButton(f"💬 Обратная связь 💬", callback_data="support_info")],
        [InlineKeyboardButton("ℹ️ О Боте ℹ️", callback_data="bot_info")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>Главное меню</b>",
        reply_markup=reply_markup,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    possibles = globals().copy()
    possibles.update(locals())
    return await possibles.get(query.data)(update, context)


async def light_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        db_q = select(Light).order_by(Light.time_created.desc())
        result = await session.execute(db_q)
        light = result.scalars().first()

    light.time_created = convert_tz(light.time_created)

    if light.value:
        text_status = "Света нет 🔴"
        text_time = "Время отключения"
    else:
        text_status = "Свет есть 🟢"
        text_time = "Время включения"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Информация на данный момент\n"
        f"📃 Статус: {text_status}\n"
        f"📆 {text_time}: {format_time(light.time_created)}",
    )


async def sub_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_status_mapping = {
        True: "Вы подписаны на уведомления 👍",
        False: "Вы не подписаны на уведомления 👎",
    }
    button_status_mapping = {
        False: [InlineKeyboardButton(f"Подписаться", callback_data="sub_me")],
        True: [InlineKeyboardButton(f"Отписаться", callback_data="unsub_me")],
    }
    query = update.callback_query

    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
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
    )


async def sub_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        db_q = select(User).where(User.tg_id == query.from_user["id"])
        result = await session.execute(db_q)
        user = result.scalars().first()
        if not user.news_subscribed:
            user.news_subscribed = True
            await session.commit()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Вы успешно подписались на уведомления ✅",
            )


async def unsub_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        db_q = select(User).where(User.tg_id == query.from_user["id"])
        result = await session.execute(db_q)
        user = result.scalars().first()
        if user.news_subscribed:
            user.news_subscribed = False
            await session.commit()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Вы успешно отписались от уведомлений ✅",
            )


async def bot_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=INFO_TEXT,
    )


async def support_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=SUPPORT_TEXT,
    )
    return SUPPORT_MSG


async def stat_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text="В разработке",
    )


async def register_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user["id"]
    text = update.message.text

    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        db_msg = Message(message=text, user_id=int(user))
        session.add(db_msg)
        await session.commit()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=f"Обращение успешно зарегистрировано ✔️",
    )

    await context.bot.send_message(
        chat_id=Cfg.ADMIN_ID,
        parse_mode=telegram.constants.ParseMode.HTML,
        text=f"‼️ <b>New message to support detected</b> ‼️\n"
        f"From: {user}\n"
        f"Msg: {text}",
    )
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_registered(update.message.from_user.id):
        return await menu(update, context)
    else:
        return await register_step_one(update, context)


async def register_step_one(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Б", "Г", "В"], ["Пропустить"]]
    await update.message.reply_text(
        REG_TEXT,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Адрес дома"
        ),
    )
    return SELECTED_HOME


async def register_step_two(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Пропустить":
        return await register_end(update, context)

    context.user_data["home"] = update.message.text
    reply_keyboard = [["Пропустить"]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ваш номер квартиры?\n(ввести цифрами)",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Номер квартиры",
        ),
        parse_mode=telegram.constants.ParseMode.HTML,
    )
    return SELECTED_FLAT


async def register_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Пропустить":
        flat = None
    else:
        flat = int(update.message.text)
    user = update.message.from_user

    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        async with session.begin():
            session.add(
                User(
                    tg_id=user.id,
                    username=user.username,
                    home=context.user_data.get("home", None),
                    flat=flat,
                )
            )
        await session.commit()
    await DB.dispose()

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Успешно зарегистрировано!"
    )
    return await start(update, context)


async def run_status_update(context: ContextTypes.DEFAULT_TYPE):
    global PREV_LIGHT_VALUE

    if PREV_LIGHT_VALUE is None:
        PREV_LIGHT_VALUE = await get_last_light_value()

    status = ping(Cfg.ROUTER_IP)
    if PREV_LIGHT_VALUE == status:
        # If no changes were noticed, just pass
        return

    async_session = sessionmaker(DB, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        db_q = select(Light.time_created).order_by(Light.time_created.desc())
        result = await session.execute(db_q)
        last_light_status = result.scalars().first()
        mins_from_prev = (
            datetime.utcnow() - last_light_status.replace(tzinfo=None)
        ).seconds // 60
        session.add(Light(value=status, mins_from_prev=mins_from_prev))
        await session.commit()
        logger.info(
            f"Created new object of Light. Switch {PREV_LIGHT_VALUE} -> {status}. Hours passed {mins_from_prev}h."
        )

    PREV_LIGHT_VALUE = status
    subscribed_users = await get_subscribed_users()

    if status:
        text = "💡 <b>Включили свет</b> 💡\n\n<i>*вы получаете это сообщение, потому что подписаны на рассылку</i>"
    else:
        text = "🚫 <b>Свет выключили</b> 🚫\n\n<i>*вы получаете это сообщение, потому что подписаны на рассылку</i>"

    for user_tg_id in subscribed_users:
        await context.bot.send_message(
            chat_id=user_tg_id, text=text, parse_mode=telegram.constants.ParseMode.HTML
        )


if __name__ == "__main__":
    app = ApplicationBuilder().token(Cfg.TG_TOKEN).build()
    job_queue = app.job_queue
    app.add_handler(
        ConversationHandler(
            entry_points=[CallbackQueryHandler(callback_handler)],
            fallbacks=[],
            states={
                SUPPORT_MSG: [MessageHandler(filters.ALL, register_support_message)]
            },
        )
    )
    app.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            fallbacks=[],
            states={
                SELECTED_NONE: [MessageHandler(filters.ALL, register_step_one)],
                SELECTED_HOME: [
                    MessageHandler(
                        filters.Regex(r"^(Б|В|Г|Пропустить)$"), register_step_two
                    )
                ],
                SELECTED_FLAT: [
                    MessageHandler(filters.Regex(r"^([0-9]{1,3})$"), register_end)
                ],
            },
        )
    )
    app.add_handler(CommandHandler("migrate", migrate))
    app.add_handler(CommandHandler("msg", msg))
    job_status_update = job_queue.run_repeating(
        run_status_update, interval=60, first=10
    )
    app.run_polling()
