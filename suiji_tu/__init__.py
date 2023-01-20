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
    if setu_random >= 0.75:
        setu_url="https://api.vvhan.com/api/tao"
    else :
        if setu_random >= 0.5:
            setu_url="https://api.wya6.cn/api/Tb_Buyer_show?return=image"
        else :
            if setu_random >= 0.25:   
                setu_url="https://api.uomg.com/api/rand.img3"
            else :
                setu_url="https://api.wya6.cn/api/Tb_Buyer_show?return=image"
    response = requests.get(setu_url)
    #response.raise_for_status()
    # response.encoding='utf-8'
    # response = response.text
    try:
        await setu.send(MessageSegment.image(response.content))
    except:
        await setu.send("欸~发送失败了喵")
    # await setu.send(Message(html))


erciyuan = on_message(rule=fullmatch({"二次元","来点二次元","二刺螈","来点二刺螈"}), priority=4, block=True)

@erciyuan.handle()
async def _():
    erciyuan_random=random.random()
    if erciyuan_random >= 0.75:
        erciyuan_url="https://api.wya6.cn/api/image_acg"
        #erciyuan_url="http://tfapi.top/API/dmt_pe.php?return=img"
    else :
        if erciyuan_random >= 0.5:
            erciyuan_url="https://api.vvhan.com/api/acgimg"
            #erciyuan_url="http://tfapi.top/API/dmt.php?return=img"
        else :
            if erciyuan_random >= 0.25:   
                #erciyuan_url="https://api.ixiaowai.cn/api/api.php"
                erciyuan_url="https://api.r10086.com/img-api.php?type=动漫综合1"
            else :
                erciyuan_url="https://api.jrsgslb.cn/acg/url.php?return=img"
    response = requests.get(erciyuan_url)
    # response.encoding='utf-8'
    # response = response.text
    try:
        await erciyuan.send(MessageSegment.image(response.content))
    except:
        await erciyuan.send("欸~发送失败了喵")
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
        await coser.send("欸~发送失败了喵")
    
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
        await xiaojiejie.send("欸~发送失败了喵")


fengjing = on_message(rule=fullmatch({"风景","来点风景"}), priority=4, block=True)
@fengjing.handle()
async def _():
    fengjing_random=random.random()
    if fengjing_random >= 0:
        fengjing_url="https://api.vvhan.com/api/view"
    else :
        fengjing_url="https://api.ixiaowai.cn/gqapi/gqapi.php"
    response = requests.get(fengjing_url)
    try:
        await fengjing.send(MessageSegment.image(response.content))
    except:
        await fengjing.send("欸~发送失败了喵")
        

Project = on_message(rule=fullmatch({"车万","东方","来点车万","来点东方"}), priority=4, block=True)
@Project.handle()
async def _():
    Project_url="https://img.paulzzh.com/touhou/random?site=all"
    response = requests.get(Project_url)
    try:
        await Project.send(MessageSegment.image(response.content))
    except:
        await Project.send("欸~发送失败了喵")    
    
Pretty = on_message(rule=fullmatch({"马娘","赛马娘","来点马娘","来点赛马娘"}), priority=4, block=True)
@Pretty.handle()
async def _():
    Pretty_url="https://api.r10086.com/img-api.php?zsy=赛马娘"
    response = requests.get(Pretty_url)
    try:
        await Pretty.send(MessageSegment.image(response.content))
    except:
        await Pretty.send("欸~发送失败了喵")      


Minecraft = on_message(rule=fullmatch({"mc","我的世界","来点mc","来点我的世界"}), priority=4, block=True)
@Minecraft.handle()
async def _():
    Minecraft_url="https://api.r10086.com/img-api.php?type=我的世界系列1"
    response = requests.get(Minecraft_url)
    try:
        await Minecraft.send(MessageSegment.image(response.content))
    except:
        await Minecraft.send("欸~发送失败了喵")
        
        

op = on_message(rule=fullmatch({"原神","来点op","来点原神"}), priority=4, block=True)
@op.handle()
async def _():
    op_url="https://api.r10086.com/img-api.php?zsy=原神"
    response = requests.get(op_url)
    try:
        await op.send(MessageSegment.image(response.content))
    except:
        await op.send("欸~发送失败了喵")        
        
        
pokemon = on_message(rule=fullmatch({"宝可梦","来点宝可梦"}), priority=4, block=True)
@pokemon.handle()
async def _():
    pokemon_url="https://api.r10086.com/img-api.php?zsy=神奇宝贝"
    response = requests.get(pokemon_url)
    try:
        await pokemon.send(MessageSegment.image(response.content))
    except:
        await pokemon.send("欸~发送失败了喵")
        
        
cat_girl = on_message(rule=fullmatch({"猫娘","来点猫娘"}), priority=4, block=True)
@cat_girl.handle()
async def _():
    cat_girl_url="https://api.r10086.com/img-api.php?type=猫娘1"
    response = requests.get(cat_girl_url)
    try:
        await cat_girl.send(MessageSegment.image(response.content))
    except:
        await cat_girl.send("欸~发送失败了喵")
        
        
frontier = on_message(rule=fullmatch({"少前","来点少前","少女前线","来点少女前线"}), priority=4, block=True)
@frontier.handle()
async def _():
    frontier_url="https://api.r10086.com/img-api.php?type=少女前线1"
    response = requests.get(frontier_url)
    try:
        await frontier.send(MessageSegment.image(response.content))
    except:
        await frontier.send("欸~发送失败了喵")        
        
arknights = on_message(rule=fullmatch({"方舟","来点方舟","明日方舟","来点明日方舟"}), priority=4, block=True)
@arknights.handle()
async def _():
    arknights_url="https://api.r10086.com/img-api.php?type=明日方舟1"
    response = requests.get(arknights_url)
    try:
        await arknights.send(MessageSegment.image(response.content))
    except:
        await arknights.send("欸~发送失败了喵")        