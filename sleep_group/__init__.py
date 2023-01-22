import asyncio
from random import choice
from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import Bot,  GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
import random
import nonebot
import os
import datetime
import time
from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json
    

sleep_group = on_command("今日陪睡", aliases={"今天陪睡"}, priority=10, block=True)
@sleep_group.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    qid = event.user_id                    # 用户ID
    group_id = event.group_id              # 群ID
    req_user_card = await get_user_card(bot, group_id,qid)       # 请求者的昵称
    # 获取群成员列表
    prep_list = await bot.get_group_member_list(group_id=group_id)
    prep_list = [prep.get("user_id", 114514) for prep in prep_list]
    prep_list.remove(qid)
    # 随机抽取幸运成员
    random.seed(hash(int(qid)))   #根据用户ID给定种子
    lucky_user = choice(prep_list)
    lucky_user_card = await get_user_card(bot, group_id, lucky_user)
    # 构造消息
    url = f"http://q1.qlogo.cn/g?b=qq&nk={lucky_user}&s=640"
    msg = (f"你今天的陪睡对象为：\n{lucky_user_card}\n" + MessageSegment.image(url))
    await sleep_group.finish(msg,at_sender=True)


sleep_group_random = on_command("陪睡", aliases={"陪睡"}, priority=10, block=True)
@sleep_group_random.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    qid = event.user_id                    # 用户ID
    group_id = event.group_id              # 群ID
    req_user_card = await get_user_card(bot, group_id,qid)       # 请求者的昵称
    #获取at对象
    qq_list = []
    data = json.loads(event.json())
    #指定陪睡对象
    for msg in data['message']:
        if msg['type'] == 'at':
            qq_list.append(int(msg['data']['qq']))
    if qq_list :
        lucky_user = choice(qq_list)
        lucky_user_card = await get_user_card(bot, group_id, lucky_user)
        # 构造消息
        url = f"http://q1.qlogo.cn/g?b=qq&nk={lucky_user}&s=640"
        msg = (f"你今天的陪睡对象为：\n{lucky_user_card}\n" + MessageSegment.image(url))
        await sleep_group_random.finish(msg,at_sender=True)
    # 获取群成员列表
    prep_list = await bot.get_group_member_list(group_id=group_id)
    prep_list = [prep.get("user_id", 114514) for prep in prep_list]
    prep_list.remove(qid)
    # 随机抽取幸运成员
    lucky_user = choice(prep_list)
    lucky_user_card = await get_user_card(bot, group_id, lucky_user)
    # 构造消息
    url = f"http://q1.qlogo.cn/g?b=qq&nk={lucky_user}&s=640"
    msg = (f"你今天的陪睡对象为：\n{lucky_user_card}\n" + MessageSegment.image(url))
    await sleep_group_random.finish(msg,at_sender=True)

async def get_user_card(bot: Bot, group_id, qid):
    # 返还用户nickname
    user_info: dict = await bot.get_group_member_info(group_id=group_id, user_id=qid)
    user_card = user_info["card"]
    if not user_card:
        user_card = user_info["nickname"]
    return user_card
    
def hash(qq: int):
    days = int(time.strftime("%d", time.localtime(time.time()))) + 31 * int(
        time.strftime("%m", time.localtime(time.time()))) + 77
    return (days * qq) >> 8