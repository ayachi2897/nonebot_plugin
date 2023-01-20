import asyncio
from random import choice
from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import Bot,  GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
import random
import nonebot
import os
from pathlib import Path

eat_group = on_command("吃群友", aliases={"吃群友"}, priority=10, block=True)


@eat_group.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    qid = event.user_id                    # 用户ID
    group_id = event.group_id              # 群ID
    req_user_card = await get_user_card(bot, group_id,qid)       # 请求者的昵称
    # 获取群成员列表
    prep_list = await bot.get_group_member_list(group_id=group_id)
    prep_list = [prep.get("user_id", 114514) for prep in prep_list]
    prep_list.remove(qid)
    eat_random = random.random()
    #群友汉堡
    if eat_random <= 0.4:
        msg = ""
        num = random.randint(3,5)
        # 随机抽取幸运成员
        lucky_user = random.sample(prep_list,num)
        #king = choice(lucky_user)
        #king = await get_user_card(bot, group_id, king)
        for i in range(0,len(lucky_user)):
            lucky_user_card = await get_user_card(bot, group_id, lucky_user[i])
            if i == len(lucky_user)-1:
                msg += f"{lucky_user_card}"
            else :    
                msg += f"{lucky_user_card}\n"
        msgs = f"恭喜你吃到了群友汉堡：\n{msg}"
        await eat_group.finish(msgs,at_sender=True)
    elif eat_random <= 0.1:
        msg = ""
        num = random.randint(5,10)
        # 随机抽取幸运成员
        lucky_user = random.sample(prep_list,num)
        #king = choice(lucky_user)
        #king = await get_user_card(bot, group_id, king)
        for i in range(0,len(lucky_user)):
            lucky_user_card = await get_user_card(bot, group_id, lucky_user[i])
            if random.random() <= 0.5:
                msg += f"{lucky_user_card}"
            else :    
                msg += f"{lucky_user_card}\n"
        msgs = f"恭喜你吃到了群友火锅：\n{msg}"
        await eat_group.finish(msgs,at_sender=True)
    # 随机抽取幸运成员
    lucky_user = choice(prep_list)
    lucky_user_card = await get_user_card(bot, group_id, lucky_user)
    # 构造消息
    url = f"http://q1.qlogo.cn/g?b=qq&nk={lucky_user}&s=640"
    msg = (f"你的这顿伙食为：\n{lucky_user_card}\n" + MessageSegment.image(url))
    await eat_group.finish(msg,at_sender=True)


async def get_user_card(bot: Bot, group_id, qid):
    # 返还用户nickname
    user_info: dict = await bot.get_group_member_info(group_id=group_id, user_id=qid)
    user_card = user_info["card"]
    if not user_card:
        user_card = user_info["nickname"]
    return user_card
    
