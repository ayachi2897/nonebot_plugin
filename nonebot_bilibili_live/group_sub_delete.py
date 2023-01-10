from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message
from pathlib import Path
import os
import json

stream_sub_delete = on_command("群直播间订阅删除")

@stream_sub_delete.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).lstrip()
    args = args.replace("群直播间订阅删除", "")
    args = args.replace(" ", "")
    if args:
        state["sentence"] = args

@stream_sub_delete.got("sentence", prompt="请输入想要删除的直播ID")
async def handle_city(bot: Bot, event: Event, state: T_State):
    sentence = state["sentence"]
    file = "/Users/28972/bot1/src/plugins/nonebot_bilibili_stream_sub/resource/sub.json"
    file_data = json.load(open(file, "r"))

    count = 0
    for i in file_data["sub"]:
        room_id = i["sub_user_id"]
        room_id = str(room_id).strip()
        room_id = room_id.replace("直播间订阅", "")
        room_id = room_id.replace(" ", "")
        print(room_id)
        print(sentence)
        if room_id == sentence:
            del file_data["sub"][count]
        count += 1
    
    with open(file, "wb+") as obj:
        obj.write(json.dumps(file_data).encode())

    await stream_sub_delete.send(Message("删除成功!"))
