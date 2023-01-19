from config.consts import EN_TO_RU_MONTH
from datetime import datetime
import pytz


def format_time(time_data) -> str:
    month = EN_TO_RU_MONTH[time_data.strftime("%B")]
    day = time_data.strftime("%-d")
    time = time_data.strftime("%H:%M")
    return f"{day} {month} {time}"


def convert_tz(time_data) -> datetime:
    return time_data.astimezone(pytz.timezone("Etc/GMT-2"))
