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
  
lolicon = on_command('来点', aliases={'来点'}, priority=20, block=True)
@lolicon.handle()
async def _(event: MessageEvent,bot: Bot):
    no_tag = ["桃宝","echo","cfm","不能转的","优质二创","滑了","烧0娜娜米","小火车","铁轨难题","古神语","可爱小七海","可爱大七海","新番"]
    lolicon_tags = str(event.get_message()).strip()
    lolicon_tags = lolicon_tags.replace("来点", "")
    lolicon_tags_url = "https://api.lolicon.app/setu/v2"
    
    if lolicon_tags in no_tag :
        await lolicon.finish()
    if lolicon_tags != "" :
        lolicon_tags = f"{lolicon_tags}"
        lolicon_tags = lolicon_tags.split( )
        lolicon_not_tag = ""
        for i in range(0,len(lolicon_tags)):
            lolicon_tag = lolicon_tags[i]
            if i == len(lolicon_tags)-1 :
                lolicon_not_tag += lolicon_tag
            else :
                lolicon_not_tag += (lolicon_tag + ',')
            if i == 0:
                lolicon_tags_url = lolicon_tags_url + '?tag=' + lolicon_tag
            else :
                lolicon_tags_url = lolicon_tags_url + '&tag=' + lolicon_tag
    response = requests.get(lolicon_tags_url)
    response.encoding='utf-8'
    response = response.text
    response = json.loads(response)
    if response['data']:
        response = response['data'][0]
        lolicon_image_url = response['urls']['original']
        lolicon_image_url = lolicon_image_url.replace('i.pixiv.re','px2.rainchan.win')
        lolicon_image = requests.get(lolicon_image_url, timeout=30)
        msg = (f"title:{response['title']}\n"
               +f"uid:{response['uid']}\n"
               +f"pid:{response['pid']}\n"
               +f"r18:{response['r18']}\n"
               +f"tags:{response['tags']}\n"
               +MessageSegment.image(lolicon_image.content)
        )
        try :
            await send_forward_msg_group(bot, event, "雪雪" ,msg)
        except:
            await lolicon.send("欸~发送失败了喵")
        #await lolicon.send(Message(msg),group_id = event.group_id, messages = msg_list)
    else :
        if lolicon_not_tag :
            msg = f"没有找到{lolicon_not_tag}呢~"
        else :
            msg = f"没有找到{lolicon_tags}呢~"
        await lolicon.send(msg)

# 合并消息
async def send_forward_msg_group(
        bot: Bot,
        event: GroupMessageEvent,
        name: str,
        msg: str,
):
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": bot.self_id, "content": msg}}

    messages = [to_json(msg)]
    try :
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    except:
        await lolicon.send("欸~发送失败了喵")
