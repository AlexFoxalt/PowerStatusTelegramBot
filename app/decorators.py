from app.logger import logger
from config.base import Config as Cfg
from functools import wraps


def admin_only(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        if update.effective_user.id != Cfg.ADMIN_ID:
            logger.info(f"Unauthorized access denied for {update.effective_user.id}.")
            return
        return await func(update, context, *args, **kwargs)

    return wrapped
