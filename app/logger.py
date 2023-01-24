import sys
from functools import lru_cache

from loguru import logger
from loguru._logger import Logger

DEFAULT_MESSAGE_FORMAT = (
    "<green>[{extra[name]}]</green> | "
    "{time:YYYY-MM-DD at HH:mm:ss} | "
    "<yellow>{level}</yellow> | "
    "<m>{function}</m> | "
    "{message}"
)
DEFAULT_LOGGER_NAME = "tg-bot"


def _setup_default_logger(context_logger: Logger) -> None:
    context_logger.add(
        sink=sys.stdout, colorize=True, format=DEFAULT_MESSAGE_FORMAT, backtrace=True
    )


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
