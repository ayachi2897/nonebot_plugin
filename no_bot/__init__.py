from nonebot import on_command
from pathlib import Path
import os
import random
from nonebot.adapters.onebot.v11 import MessageSegment

yydz = on_command('帮助', aliases={'帮助'}, priority=4, block=True)

img_path = Path(os.path.join(os.path.dirname(__file__), "resource"))
all_file_name = os.listdir(str(img_path))


@yydz.handle()
async def wte():
    img_name = random.choice(all_file_name)
    img = img_path / img_name
    msg=(
        f"咱才不是机器人了啦\n"
        +MessageSegment.image(img)
    )
    await yydz.send(msg)

