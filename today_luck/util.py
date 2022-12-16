import datetime
from typing import Type

from nonebot.internal.matcher import Matcher


def get_wife_date() -> datetime.date:
    _datetime = datetime.datetime.today()
    date = _datetime.date()
    hour = _datetime.time().hour
    if 0 <= hour < 6:
        return date - datetime.timedelta(days=1)
    else:
        return date


async def wife_date_remind(matcher: Type[Matcher]) -> None:
    if datetime.date.today() != get_wife_date():
        await matcher.send('早上六点才会刷新噢，早点休息吧~')
