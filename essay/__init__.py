import shlex
from typing import Type
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message

from .data_source import commands, get_essay


__zx_plugin_name__ = "CP文等多种短文生成"
__plugin_usage__ = """
usage：
    CP文等多种短文生成
    指令：
      苏联笑话 {要讽刺的事} {谁提出来的} {有助于什么} {针对的是谁} {起作用范围}
      CP文 攻 受
      营销号 {主题} {描述} {另一种描述}
      毒鸡汤
      藏头诗
""".strip()
__plugin_des__ = "CP文等多种短文生成"
__plugin_type__ = ("群内小游戏",)
__plugin_cmd__ = ["CP文、毒鸡汤、藏头诗 等"]
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["CP文等多种短文生成"],
}






async def handle(matcher: Type[Matcher], type: str, text: str):
    arg_num = commands[type].get("arg_num", 1)
    texts = shlex.split(text) if arg_num > 1 else [text]
    if not arg_num:
        texts = []
    elif arg_num != len(texts):
        await matcher.finish(f"Usage:\n{commands[type]['help']}")
    res = await get_essay(type, texts)
    if res:
        await matcher.finish(res)
    else:
        await matcher.finish("出错了，请稍后再试")


def create_matchers():
    def create_handler(type: str) -> T_Handler:
        async def handler(msg: Message = CommandArg()):
            text = msg.extract_plain_text().strip()
            await handle(matcher, type, text)

        return handler

    for type, params in commands.items():
        matcher = on_command(type, aliases=params["aliases"], block=True, priority=5)
        matcher.append_handler(create_handler(type))


create_matchers()
