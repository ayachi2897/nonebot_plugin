from nonebot import on_metaevent
from nonebot.plugin.on import on_message,on_notice,on_command
from nonebot.rule import to_me,keyword
from pathlib import Path
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Message,MessageSegment,Bot,Event
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN,GROUP_MEMBER
from nonebot.permission import SUPERUSER
from nonebot.rule import Rule
import os
import json

def write_group_data() -> None:
    with open("data/group_white/group_white.json", "w", encoding="utf-8") as f:
        json.dump(group_white, f, indent=4)

#白名单
async def is_enable(event: GroupMessageEvent) -> bool:
    gid = event.group_id
    group_black = []
    if gid in group_black:
        return gid in group_black
    else:
        if str(gid) not in group_white:
            return gid not in [436304487,285191524,477690692,240469024,710485130,828050941]
        else:
            return group_white[str(gid)]["allow"] == False
# #黑名单
# async def is_enable(event: Event) -> bool:
    # group = [689688087,818812772]
    # return event.group_id  in group
    
rule = Rule(is_enable)    
date = on_message(rule = rule,block=True,priority=0) 
   
@date.handle()
async def _():
        return

    
white = on_command("关闭bot",aliases={"开启bot","启用bot","禁用bot"},priority=0,permission=(SUPERUSER | GROUP_ADMIN | GROUP_OWNER))
@white.handle()
async def _(event: GroupMessageEvent):
    # 获取消息文本
    msg = str(event.get_message())
    gid = str(event.group_id)  # 群号
    if msg == "开启bot" or msg == "启用bot":
        if gid in group_white:
            group_white[gid]["allow"] = True
            write_group_data()
            await white.finish("bot已开启喵")
        else:
            group_white.update({gid: {"allow": True}})
            write_group_data()
            await white.finish("bot已开启喵")
    elif msg == "关闭bot" or msg == "禁用bot":
        if gid in group_white:
            group_white[gid]["allow"] = False
            write_group_data()
            await white.finish("bot已禁用喵")
        else:
            group_white.update({gid: {"allow": False}})
            write_group_data()
            await white.finish("bot已禁用喵")
        
# 读取群配置, 可能有人要问了, 为什么要搞这么多个json, 因为我自己的bot上个数据有多个用户数据, 我懒得合并了
if os.path.exists("data/group_white/group_white.json"):  # 读取用户数据
    with open("data/group_white/group_white.json", "r", encoding="utf-8") as f:
        group_white = json.load(f)
else:   # 不存在则创建
    if not os.path.exists("data/group_white"):
        os.makedirs("data/group_white")  # 创建文件夹
    group_white = {}
            
            
            
