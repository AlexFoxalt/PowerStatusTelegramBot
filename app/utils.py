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


def get_hours_and_mins(mins) -> str:
    return f"{mins // 60}ч.{mins % 60}мин."


def get_date_and_month(time_data) -> str:
    return f"{time_data.strftime('%-d')} {EN_TO_RU_MONTH[time_data.strftime('%B')]}"


def get_percent_of_two(x: int, from_y: int) -> float:
    return round((x - from_y) / from_y * 100)
