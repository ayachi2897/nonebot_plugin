import random

from nonebot import on_command, on_regex
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent,MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Arg, ArgPlainText, CommandArg, EventMessage

jueding = on_command("帮我选择", aliases={"帮我选择"}, priority=1)


@jueding.handle()
async def handle_first_receive(matcher: Matcher, state, arg: Message = CommandArg()):
    args = arg
    # await jueding.send(f"args = {args}")
    if args:
        matcher.set_arg("xuanze", args)


@jueding.got("xuanze", prompt="请输入需要雪雪帮你决定的内容（用空格分开）:")
async def handle_xuanze(xuanze: str = ArgPlainText("xuanze")):
    # await jueding.send(f"xuanze = {xuanze}")
    out = "雪雪认为你应该选择: " + str(random.choice(xuanze.split()))
    await jueding.finish(out,reply_message = True)
    
    
    
XuanZe = on_regex(r"(.*?)(还是)(.*?)",rule = to_me(),priority=1,block=True)
@XuanZe.handle()
async def _(event: MessageEvent):
    msgs = str(event.get_message()).strip()
    msg = msgs.split("还是")
    Shiro = random.choice(msg)
    if Shiro.find("CQ:image") == -1:
        msg = "雪雪认为你应该选择: " + Shiro
    else:
        msg = "雪雪认为你应该选择: " + Message(Shiro)
    await XuanZe.finish(msg,reply_message = True)
