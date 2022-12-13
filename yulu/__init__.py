from nonebot.plugin.on import on_message
from nonebot.rule import fullmatch
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageEvent,
)
from .utils import *


ai = on_message(rule=fullmatch({"随机语录","语录"}), priority=5, block=True)


@ai.handle()
async def _(event: MessageEvent):
    # 获取消息文本
    msg = str(event.get_message())
    # 去掉带中括号的内容(去除cq码)
    msg = re.sub(r"\[.*?\]", "", msg)
    # 从LeafThesaurus里获取结果
    result = await get_chat_result_leaf(msg)
    await ai.finish(Message(result))

