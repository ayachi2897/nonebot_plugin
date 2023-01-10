from nonebot import on_message
from nonebot.rule import keyword
from nonebot.adapters.onebot.v11 import Message,MessageEvent
import requests
import re



dianying = on_message(rule=keyword("电影"), priority=4, block=True)


@dianying.handle()
async def _(event: MessageEvent):
    diany = str(event.get_message()).strip()
    diany = diany.replace("电影", "")
    diany = diany.replace(" ", "")
    data = diany
    url= "http://tfapi.top/API/dy.php"
    url= url + '?&msg=' + data + '&n=1'
    response = requests.get(url)
    response.encoding='utf-8'
    html = response.text
    await dianying.send(Message(html))
