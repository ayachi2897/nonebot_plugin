from nonebot import on_message,on_regex
from nonebot.rule import fullmatch
from nonebot.adapters.onebot.v11 import Message,MessageSegment
import requests
import re
import random



setu = on_message(rule=fullmatch({"买家秀","来点买家秀"}), priority=15, block=True)

@setu.handle()
async def _():
    setu_random=random.random()
    if setu_random >= 0:
        setu_url="http://tfapi.top/API/nypic.php?return=img"
    else:
        setu_url="http://tfapi.top/API/yht.php?return=txt"
        setu_url = requests.get(setu_url)
        setu_url=setu_url.text
    response = requests.get(setu_url)
    response.raise_for_status()
    # response.encoding='utf-8'
    # response = response.text
    try:
        await setu.send(MessageSegment.image(response.content))
    except:
        await setu.send("发送失败")
    # await setu.send(Message(html))


erciyuan = on_message(rule=fullmatch({"二次元","来点二次元","二刺螈","来点二刺螈"}), priority=4, block=True)

@erciyuan.handle()
async def _():
    erciyuan_random=random.random()
    if erciyuan_random >= 0.8:
        erciyuan_url="http://tfapi.top/API/dmt_pe.php?return=img"
    else :
        if erciyuan_random >= 0.6:
            erciyuan_url="http://tfapi.top/API/dmt.php?return=img"
        else :
            if erciyuan_random >= 0.4:   
                erciyuan_url="http://tfapi.top/API/setu_pic.php?return=img"
            else :
                erciyuan_url="https://api.jrsgslb.cn/acg/url.php?return=img"
    response = requests.get(erciyuan_url)
    # response.encoding='utf-8'
    # response = response.text
    try:
        await erciyuan.send(MessageSegment.image(response.content))
    except:
        await erciyuan.send("发送失败")
    # await setu.send(Message(html))


#coser = on_regex(r"^(\d)?连?(cos|COS|coser|括丝)$", priority=5, block=True)
coser = on_message(rule=fullmatch({"cos","COS","来点cos","来点COS"}), priority=4, block=True)
@coser.handle()
async def _():
    coser_random=random.random()
    if coser_random >= 2:
        coser_url="https://picture.yinux.workers.dev"
    else :
        coser_url="https://api.jrsgslb.cn/cos/url.php?return=img"
    response = requests.get(coser_url)
    # response.encoding='utf-8'
    # response = response.text
    try:
        await coser.send(MessageSegment.image(response.content))
    except:
        await coser.send("发送失败")
    
xiaojiejie = on_message(rule=fullmatch({"小姐姐","来点小姐姐","三次元","来点三次元"}), priority=4, block=True)
@xiaojiejie.handle()
async def _():
    xiaojiejie_url="https://api.jrsgslb.cn/kt/url.php?return=img"
    response = requests.get(xiaojiejie_url)
    # response.encoding='utf-8'
    # response = response.text
    try:
        await xiaojiejie.send(MessageSegment.image(response.content))
    except:
        await xiaojiejie.send("发送失败")