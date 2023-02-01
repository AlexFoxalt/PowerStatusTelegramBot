import sys
from functools import lru_cache
from zoneinfo import ZoneInfo

import telegram
from loguru import logger
from loguru._logger import Logger

DEFAULT_MESSAGE_FORMAT = (
    "<yellow>{level}</yellow> | "
    "<g><i>{extra[datetime]:YYYY-MM-DD at HH:mm:ss}</i></g> | "
    "<m><b>{function}</b></m> | "
    "{message}"
)
DEFAULT_LOGGER_NAME = "tg-bot"


def ignore_error(record):
    if record["exception"] is not None:
        _, exc, _ = record["exception"]
        if isinstance(exc, telegram.error.NetworkError):
            return False
    return True


def set_datetime(record):
    dt = record["time"]
    eet = ZoneInfo("EET")
    eettime = dt.astimezone(eet)
    record["extra"]["datetime"] = eettime


def _setup_default_logger(context_logger: Logger) -> None:
    context_logger.add(
        sink=sys.stdout,
        colorize=True,
        format=DEFAULT_MESSAGE_FORMAT,
        backtrace=True,
        filter=ignore_error,
    )
    context_logger.configure(patcher=set_datetime)


def _setup_logger(name: str) -> Logger:
    """
    Return configured logger.
    """
    logger.remove()
    context_logger = logger.bind(name=name)
    _setup_default_logger(context_logger)
    return context_logger


@lru_cache(maxsize=None)
def get_logger(name: str = DEFAULT_LOGGER_NAME) -> Logger:
    """
    Initialize logger for project.
    """
    return _setup_logger(name)
