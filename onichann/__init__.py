from nonebot import on_command
from pathlib import Path
import os
import random
from nonebot.adapters.onebot.v11 import MessageSegment

onichann = on_command('欧尼酱', aliases={'来点欧尼酱','真寻','来点真寻'}, priority=4, block=True)


img_path = Path(os.path.join(os.path.dirname(__file__), "resource"))
all_file_name = os.listdir(str(img_path))


@onichann.handle()
async def _():
    img_name = random.choice(all_file_name)
    img = img_path / img_name
    try:
        await onichann.send(MessageSegment.image(img))
    except:
        await onichann.send("发送失败")
