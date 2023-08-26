from nonebot import on_regex,on_command
from pathlib import Path
import os
import random
from nonebot.adapters.onebot.v11 import MessageSegment, Event
import requests


what_eat=on_regex(r"(今?(天|晚)|早上|晚上|中午|夜宵)?吃什么$",priority=1,block=True)
what_drink=on_regex(r"(今?(天|晚)|早上|晚上|中午|夜宵)?喝什么$",priority=1,block=True)

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
        
        
        
eat_add = on_command("添加吃什么菜单",priority=1,block=True)
@eat_add.handle()
async def save_image(event: Event):
    all_file_name = os.listdir(str(img_path))
    image = None
    text = None
    for segment in event.message:
        if segment.type == "image":
            image = segment
        if segment.type == "text":
            text = str(segment).strip().replace("添加吃什么菜单", "") + ".jpg"
    if text in all_file_name:
            await eat_add.finish("该菜名已存在")        
    if image and text != ".jpg":
        image_url = image.data.get("url")
        save_path = os.path.join(img_path, text)  # 拼接保存路径

        # 使用Requests库下载图片
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            
            await eat_add.finish("菜单添加成功")
        else:
            await eat_add.finish("菜单添加失败")
    else:
        if not image:
            await eat_add.finish("没有图怎么添加，你个笨蛋")
        if text == ".jpg":
            await eat_add.finish("名字呢，你个笨蛋")


eat_remove = on_command("删除吃什么菜单",priority=1,block=True)
@eat_remove.handle()
async def save_image(event: Event):
    name = str(event.message).strip().replace("删除吃什么菜单", "")
    file_path = os.path.join(img_path, name+".jpg")
    try:
        # 删除文件
        os.remove(file_path)
        await eat_remove.send(f'{name}已成功删除')
    except FileNotFoundError:
        await eat_remove.send(f'{name}不存在')
    except Exception as e:
        await eat_remove.send(f'删除菜单时发生错误：{e}')
