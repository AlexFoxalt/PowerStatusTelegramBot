import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ROUTER_IP = os.getenv("ROUTER_IP")
    TG_TOKEN = os.getenv("TG_TOKEN")
    POSTGRES_DSN = os.getenv("POSTGRES_DSN")
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
    TICKS_BETWEEN_PINGS = 60
