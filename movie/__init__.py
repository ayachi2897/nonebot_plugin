from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message,MessageSegment,MessageEvent,GroupMessageEvent
from nonebot.adapters.onebot.v11.bot import Bot
import requests
import re
import random
try:
    import ujson as json
except ModuleNotFoundError:
    import json
  
movie = on_command('影视', aliases={'电视剧'}, priority=4, block=True)
@movie.handle()
async def _(event: MessageEvent,bot: Bot):
    movie_seed = str(event.get_message()).strip()
    movie_seed = movie_seed.replace("影视", "")
    movie_seed = movie_seed.replace("电视剧", "")
    movie_seed = movie_seed.replace(" ", "")
    movie_seed_url = "https://wenxin110.top/api/movie_search?msg="
    movie_seed_url += movie_seed
    response = requests.get(movie_seed_url)
    response.encoding='utf-8'
    response = response.text
    response = json.loads(response)
    msgs = None
    msgs = [msgs]
    if response['code'] == 1 :
        for i in range(0,len(response['result'])):
            msg = (f"{response['result'][i]['from']}\n{response['result'][i]['title']}\n{response['result'][i]['url']}")
            #await movie.send(msg)
            msg = [msg]
            msgs += msg
        #print(msgs)
        await send_forward_msg_group(bot, event, "雪雪" ,msgs)
        #await movie.send(Message(msg),group_id = event.group_id, messages = msg_list)


# 合并消息
async def send_forward_msg_group(
        bot: Bot,
        event: GroupMessageEvent,
        name: str,
        msgs: [],
):
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": bot.self_id, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=messages
    )