import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    ENV = os.getenv("ENV")

    ROUTER_IP = os.getenv("ROUTER_IP")
    TG_TOKEN = os.getenv("TG_TOKEN")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT") if ENV != "local" else 5433
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DSN = (
        f"postgresql+asyncpg://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
    TICKS_BETWEEN_PINGS = 60

    DTEK_SCHEDULE_NAME = "dtek_schedule.png"
    DEFAULT_PINNED_MSG = "Default message"

    # UTC Time
    DISABLE_SOUND_START_TIME = 22
    DISABLE_SOUND_END_TIME = 6

    @classmethod
    def get_dtek_media(self):
        return open(f"./media/{self.DTEK_SCHEDULE_NAME}", "rb")
