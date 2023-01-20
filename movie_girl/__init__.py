from nonebot import on_message,on_regex
from nonebot.rule import fullmatch
from nonebot.adapters.onebot.v11 import Message,MessageSegment
import requests
import re
import random
import os
from pathlib import Path

 
movie = on_message(rule=fullmatch({"来点抖音","来点视频"}), priority=4, block=True)
@movie.handle()
async def _():
    movie_seed_url = "http://api.zixuan.ink/API/sjmn.php"
    response = requests.get(movie_seed_url)
    #response.encoding='utf-8'
    response = response.content
    with open(r'C:\Users\28972\bot1\src\plugins\movie_girl\resource\1.mp4', mode = 'wb') as f:
        # 获取pic的二进制内容,写入f
        f.write(response)
    video_path = Path(os.path.join(os.path.dirname(__file__), "resource"))
    video_name = os.listdir(str(video_path))
    print(video_name)
    video = video_path / video_name[0]
    try:
        await movie.send(MessageSegment.video(video))
    except:
        await movie.send("欸~发送失败了喵") 
    