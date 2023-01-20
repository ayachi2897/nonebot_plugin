import asyncio
from random import choice
from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import Bot,  GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
import random
import nonebot
import os
from pathlib import Path

imparty = on_command("开群淫趴", aliases={"开淫趴"}, priority=10, block=True)


@imparty.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    qid = event.user_id                    # 用户ID
    group_id = event.group_id              # 群ID
    req_user_card = await get_user_card(bot, group_id,qid)       # 请求者的昵称
    # 获取群成员列表
    prep_list = await bot.get_group_member_list(group_id=group_id)
    prep_list = [prep.get("user_id", 114514) for prep in prep_list]
    msg = ""
    # 随机抽取幸运成员
    prep_list_num = len(prep_list)
    print(prep_list_num)
    if prep_list_num < 20 :
        num = 4
    else :
        num = 9
    qids = [qid]
    lucky_user = random.sample(prep_list,num)
    lucky_user += qids
    #king = choice(lucky_user)
    #king = await get_user_card(bot, group_id, king)
    for i in range(0,len(lucky_user)):
        lucky_user_card = await get_user_card(bot, group_id, lucky_user[i])
        if i == len(lucky_user)-1:
            msg += f"{i+1}.{lucky_user_card}"
        else :    
            msg += f"{i+1}.{lucky_user_card}\n"
    msgs = f"参与本次淫趴的美少女为：\n{msg}\n其中本次淫趴的主角为：\n⭐⭐⭐{req_user_card}⭐⭐⭐"
    await imparty.finish(msgs)


async def get_user_card(bot: Bot, group_id, qid):
    # 返还用户nickname
    user_info: dict = await bot.get_group_member_info(group_id=group_id, user_id=qid)
    user_card = user_info["card"]
    if not user_card:
        user_card = user_info["nickname"]
    return user_card
    

    