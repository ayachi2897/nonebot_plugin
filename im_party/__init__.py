import asyncio
from random import choice
from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import Bot,  GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
import random
import nonebot
import os
from pathlib import Path
import time


#最大支持玩家数
max_player = 10
#最少玩家数
min_player = 3
race = {}  
imparty_new = on_command("发起群淫趴", aliases={"发起淫趴"}, priority=10, block=True)

@imparty_new.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global race
    group = event.group_id
    uid = event.user_id                    # 用户ID
    user_card = await get_user_card(bot, group,uid)       # 请求者的昵称
    try:
        if race[group].start == 0 and time.time() - race[group].time < 300:
            out_msg = f"已有发起的淫趴喵~"
            await imparty_new.finish(out_msg)
        elif race[group].start == 1 :
            await imparty_new.finish(f"一场淫趴正在进行中")
            await imparty_new.finish()
    except KeyError:
        pass
    race[group] = race_group()
    await imparty_new.finish(f"{user_card}发起了群淫趴\n输入“加入淫趴”以参与本次淫趴喵~")
    
    
imparty_join = on_command("加入淫趴", aliases={"加入群淫趴"}, priority=10, block=True)    
@imparty_join.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global race, max_player
    uid = event.user_id
    group = event.group_id
    player_name = event.sender.card if event.sender.card else event.sender.nickname
    try:
        race[group]
    except KeyError:
        await imparty_join.finish( f"淫趴未举办\n请输入“发起淫趴”举办一场淫趴喵~")
    try:
        if race[group].start == 1 or race[group].start == 2:
            await imparty_join.finish()
    except KeyError:
        await imparty_join.finish()
    if race[group].query_of_player() >= max_player:
        await imparty_join.finish( f"趴场就那么大，满了喵~" )
    if race[group].is_player_in(uid) == True:
        await imparty_join.finish( f"您已经加入了淫趴喵~")
    race[group].add_player(uid, player_name)
    out_msg = f"加入淫趴成功"
    await imparty_join.finish(out_msg, at_sender=True)   

imparty_start = on_command("开始淫趴", aliases={"开始群淫趴","开趴","淫趴开始","群淫趴开始"}, priority=10, block=True)     
@imparty_start.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global race
    global events_list
    group = event.group_id
    try:
        if race[group].query_of_player() == 0:
            await imparty_start.finish()
    except KeyError:
        await imparty_start.finish()
    try:
        if race[group].start == 0 or race[group].start == 2:
            if len(race[group].player) >= min_player:
                race[group].start_change(1)
            else:
                await imparty_start.finish(f'淫趴需要最少{str(min_player)}人参与喵~', at_sender=True)
        elif race[group].start == 1:
            await imparty_start.finish()
    except KeyError:
        await imparty_start.finish()
    race[group].time = time.time()
    while race[group].start == 1:  
        imparty_user = []   
        for i in range(0,len(race[group].player)):
            imparty_player = [race[group].player[i].player]
            imparty_user += imparty_player
        king = choice(imparty_user)
        msg = ""
        for ii in range(0,len(imparty_user)):
            if ii == len(imparty_user)-1:
                msg += f"{ii+1}.{imparty_user[ii]}"
            else :    
                msg += f"{ii+1}.{imparty_user[ii]}\n"
            msgs = f"参与本次淫趴的美少女为：\n{msg}\n其中本次淫趴的主角为：\n⭐⭐⭐{king}⭐⭐⭐"
        del race[group]
        await imparty_start.finish(msgs)
    
    
    
class race_group:
#初始化
    def __init__(self):
        self.player = []
        self.round = 0
        self.start = 0
        self.time = time.time()
        self.race_only_keys = []
#start指示器变更 0为马儿进场未开始，1为开始，2为暂停（测试用）
    def start_change(self, key):
        self.start = key
#增加赛马位
    def add_player(self, uid = 114514, id = "the_player",location = 0, round = 0):
        self.player.append(horse(uid, id, location, round))
#赛马位数量查看
    def query_of_player(self):
        return len(self.player)
#查找有无玩家
    def is_player_in(self, uid):
        for i in range(0, len(self.player)):
            if self.player[i].playeruid == uid:
                return True
                
                
class horse:
    def __init__(self, uid = 114514, id = "the_player", location = 0, round = 0 ):
        self.playeruid = uid
        self.player =  id
        self.buff = []
        self.delay_events = []
        self.round = round
        self.location = location
        self.location_add = 0
        self.location_add_move = 0




                
async def get_user_card(bot: Bot, group_id, qid):
    # 返还用户nickname
    user_info: dict = await bot.get_group_member_info(group_id=group_id, user_id=qid)
    user_card = user_info["card"]
    if not user_card:
        user_card = user_info["nickname"]
    return user_card                
    
    
   