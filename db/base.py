from sqlalchemy.ext.asyncio import create_async_engine
from config.base import Config as Cfg

DB = create_async_engine(Cfg.POSTGRES_DSN)
