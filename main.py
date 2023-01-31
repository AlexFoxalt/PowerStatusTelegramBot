from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

import app.handlers as handler
from app.logger import get_logger
from app.tasks import run_status_update
from config.base import Config as Cfg

logger = get_logger(__name__)


if __name__ == "__main__":
    app = ApplicationBuilder().token(Cfg.TG_TOKEN).build()
    job_queue = app.job_queue
    app.add_handler(
        ConversationHandler(
            entry_points=[CallbackQueryHandler(handler.callback_handler)],
            fallbacks=[CallbackQueryHandler(handler.callback_handler)],
            states={
                handler.SUPPORT_MSG: [
                    MessageHandler(
                        filters.ALL, handler.register_support_message
                    )
                ]
            },
        )
    )
    app.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("start", handler.start)],
            fallbacks=[],
            states={
                handler.SELECTED_NONE: [
                    MessageHandler(filters.ALL, handler.register_step_one)
                ],
                handler.SELECTED_HOME: [
                    MessageHandler(
                        filters.Regex(r"^(8Б|8В|8Г|Пропустить)$"),
                        handler.register_step_two,
                    )
                ],
                handler.SELECTED_FLAT: [
                    MessageHandler(
                        filters.Regex(r"^([0-9]{1,3}|Пропустить)$"),
                        handler.register_end,
                    )
                ],
            },
        )
    )

    app.add_handler(CommandHandler("migrate", handler.migrate))
    app.add_handler(CommandHandler("msg", handler.msg))
    app.add_handler(CommandHandler("msgpin", handler.msgpin))
    app.add_handler(CommandHandler("msgall", handler.msgall))
    # job_status_update = job_queue.run_repeating(
    #     run_status_update, interval=60, first=60
    # )
    logger.info("Bot starting")
    app.run_polling(timeout=30)
