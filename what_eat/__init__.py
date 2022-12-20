from nonebot import on_regex
from pathlib import Path
import os
import random
from nonebot.adapters.onebot.v11 import MessageSegment

what_eat=on_regex(r"(今?(天|晚)|早上|晚上|中午|夜宵)?吃什么$",priority=5,block=True)
what_drink=on_regex(r"(今?(天|晚)|早上|晚上|中午|夜宵)?喝什么$",priority=5,block=True)

img_path = Path(os.path.join(os.path.dirname(__file__), "resource"))
all_file_name = os.listdir(str(img_path))


@what_eat.handle()
async def wte():
    img_name = random.choice(all_file_name)
    img = img_path / img_name
    msg=(
        f"去吃{img.stem}吧\n"
        +MessageSegment.image(img)
    )
    try:
        await what_eat.send(msg,at_sender=True)
    except:
        await what_eat.finish(message="出错啦！没有找到好吃的~")


imgs_path = Path(os.path.join(os.path.dirname(__file__), "drink_pic"))
alls_file_name = os.listdir(str(imgs_path))

@what_drink.handle()
async def wte():
    img_name = random.choice(alls_file_name)
    img = imgs_path / img_name
    msg=(
        f"来喝{img.stem}吧\n"
        +MessageSegment.image(img)
    )
    try:
        await what_drink.send(msg,at_sender=True)
    except:
        await what_drink.finish(message="出错啦！没有找到好吃的~")
