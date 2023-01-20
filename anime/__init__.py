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
  
anime = on_command('搜番', aliases={'动漫'}, priority=4, block=True)
@anime.handle()
async def _(event: MessageEvent,bot: Bot):
    anime_seed = str(event.get_message()).strip()
    anime_seed = anime_seed.replace("搜番", "")
    anime_seed = anime_seed.replace("动漫", "")
    anime_seed = anime_seed.replace(" ", "")
    anime_seed_url = "https://ybapi.cn/API/acg_1.php?name="
    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    anime_seed_url += anime_seed
    response = requests.get(anime_seed_url,headers=headers)
    response.encoding='utf-8'
    response = response.text
    data = re.compile('\[换行\](\d+)')
    data = data.findall(response)
    data = [data]
    #data = data.split('.')
    #print(data)
    #print(len(data[0]))
    msgs = None
    msgs = [msgs]
    for i in range(0,len(data[0])):
        anime_url = "https://ybapi.cn/API/acg_2.php?id="
        anime_url += data[0][i]
        #print(anime_url)
        anime_response = requests.get(anime_url)
        anime_response.encoding='utf-8'
        anime_response = anime_response.text
        anime_response = json.loads(anime_response)
        #print(anime_response)
        anime_image_url = anime_response['image']
        anime_image = requests.get(anime_image_url)
        msg = (f"{anime_response['name']}\n{anime_response['url']}\n" + MessageSegment.image(anime_image.content) + '\n')
        msg = [msg]
        msgs += msg
        print(msgs)
    await send_forward_msg_group(bot, event, "雪雪" ,msgs)
        #await anime.send(Message(msg),group_id = event.group_id, messages = msg_list)


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