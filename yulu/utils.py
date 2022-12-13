import os
import re
import random
import nonebot

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from httpx import AsyncClient
from pathlib import Path
from nonebot.adapters.onebot.v11 import Message, MessageSegment


path = os.path.join(os.path.dirname(__file__), "resource")




# 载入首选词库
LeafThesaurus = json.load(open(Path(path) / "leaf.json", "r", encoding="utf8"))


async def get_chat_result_leaf(text: str) -> str:
    '''
    从LeafThesaurus里返还消息
    '''
    if len(text) < 500:
        keys = LeafThesaurus.keys()
        for key in keys:
            if text.find(key) != -1:
                return random.choice(LeafThesaurus[key])



def is_CQ_Code(msg:str) -> bool:
    '''
    判断参数是否为CQ码
    '''
    if len(msg) > 4 and msg[0] == '[' and msg[1:4] == "CQ:" and msg[-1] == ']':
        return True
    else:
        return False

def messagePreprocess(msg: Message):
    '''
    对CQ码返回文件名（主要是处理CQ:image）
    '''
    msg = str(msg)
    if is_CQ_Code(msg):
        data = msg.split(',')
        for x in data:
            if "file=" in x:
                return x
    return msg

