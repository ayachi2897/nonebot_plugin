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
  
calories = on_command('卡路里查询', aliases={'查询卡路里'}, priority=4, block=True)
@calories.handle()
async def _(event: MessageEvent,bot: Bot):
    calories_seed = str(event.get_message()).strip()
    calories_seed = calories_seed.replace("卡路里", "")
    calories_seed = calories_seed.replace("查询", "")
    calories_seed = calories_seed.replace(" ", "")
    calories_seed_url = "http://api.zixuan.ink/API/calories.php?food="
    calories_seed_url += calories_seed
    response = requests.get(calories_seed_url)
    response.encoding='utf-8'
    response = response.text
    response = json.loads(response)
    msgs = None
    msgs = [msgs]
    if response['msg'] == "获取成功" :
        msgs = msgs + [f"查询到了{len(response['data'])}中食物呢~"]
        for i in range(0,len(response['data'])):
            msg = (f"{response['data'][i]['food']}：\n{response['data'][i]['calories']}")
            #await calories.send(msg)
            msg = [msg]
            msgs += msg
        #print(msgs)
        await send_forward_msg_group(bot, event, "雪雪" ,msgs)
        #await calories.send(Message(msg),group_id = event.group_id, messages = msg_list)
    else :
        await calories.send(f"没有查询到{calories_seed}呢~")

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
