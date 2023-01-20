from nonebot import on_command
from pathlib import Path
import os
import random
from nonebot.adapters.onebot.v11 import MessageSegment

LianBao = on_command('莲宝骂我', aliases={'东雪莲骂我','罕见骂我'}, priority=4, block=True)


img_path = Path(os.path.join(os.path.dirname(__file__), "resource"))
all_file_name = os.listdir(str(img_path))


@LianBao.handle()
async def _():
    img_name = random.choice(all_file_name)
    img = img_path / img_name
    try:
        await LianBao.send(MessageSegment.record(img))
    except:
        await LianBao.send("欸~发送失败了喵")
