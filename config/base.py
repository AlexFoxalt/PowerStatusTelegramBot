import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ROUTER_IP = os.getenv("ROUTER_IP")
    TG_TOKEN = os.getenv("TG_TOKEN")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
    TICKS_BETWEEN_PINGS = 60

    DEFAULT_PINNED_MSG = "Default message"
