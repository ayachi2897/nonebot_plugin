from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message,MessageSegment,MessageEvent,GroupMessageEvent
from nonebot.adapters.onebot.v11.bot import Bot
import requests
import re
import random
import os
from pathlib import Path
import base64
try:
    import ujson as json
except ModuleNotFoundError:
    import json

aidraw = on_command('绘图', aliases={'绘图'}, priority=20, block=True)
@aidraw.handle()
async def _(event: MessageEvent,bot: Bot):
    aidraw_tags = str(event.get_message()).strip()
    aidraw_tags = aidraw_tags.replace("绘图", "")
    aidraw_tags_url = "https://wakuwaku.azurewebsites.net/api/ai"
    if aidraw_tags != "" :
        aidraw_tags = f"{aidraw_tags}"
        aidraw_tags = aidraw_tags.split( )
        if len(aidraw_tags) == 1 :
            aidraw_tag = aidraw_tags[0]
            aidraw_tags_url = aidraw_tags_url + f"?tag=[{aidraw_tag}]"
            #print(aidraw_tags_url)
        else:
            for i in range(0,len(aidraw_tags)):
                aidraw_tag = aidraw_tags[i]
                if i == 0 :
                    aidraw_tags_url = aidraw_tags_url + f"?tag=[{aidraw_tag},"
                else :
                    if i == len(aidraw_tags)-1:
                        aidraw_tags_url = aidraw_tags_url + f"{aidraw_tag}]"
                    else :
                        aidraw_tags_url = aidraw_tags_url + f"{aidraw_tag},"
                #print(aidraw_tags_url)

    else :
        await aidraw.finish("tag呢？")
    aidraw_image = requests.get(aidraw_tags_url)
    aidraw_image.encoding = 'utf-8'
    aidraw_image = aidraw_image.content
    aidraw_image = str(aidraw_image).strip()
    aidraw_image = aidraw_image.replace("b'<img src=\"data:image/png;base64,", "")
    aidraw_image = aidraw_image.replace("\"/>'", "")
    aidraw_image += '=='
    aidraw_image = base64.b64decode(aidraw_image)
    with open(r'C:/Users/28972/bot1/src/plugins/mengyu_aidraw/resource/1.jpg', mode = 'wb') as png:
        png.write(aidraw_image)
    video_path = Path(os.path.join(os.path.dirname(__file__), "resource"))
    video_name = os.listdir(str(video_path))
    img = video_path / video_name[0]
    try :
        await aidraw.send(MessageSegment.image(img))
    except:
        await aidraw.send("欸~发送失败了喵")
