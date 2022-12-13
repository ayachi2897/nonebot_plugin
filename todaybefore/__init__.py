from nonebot.rule import T_State
from nonebot import on_command, require, get_driver, get_bot
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from .config import Config
from .data_source import get_todaybefore

__zx_plugin_name__ = "历史上的今天"
__plugin_usage__ = """
usage：
    历史上的今天
    指令：
       历史上的今天
""".strip()
__plugin_des__ = "历史上的今天"
__plugin_type__ = ("群内小游戏",)
__plugin_cmd__ = ["]"]
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["历史上的今天"],
}

global_config = get_driver().config
config = Config(**global_config.dict())
nickname = list(global_config.nickname)
admin = list(global_config.superusers)
scheduler = require("nonebot_plugin_apscheduler").scheduler
todaybefore = on_command("yuki历史上的今天", priority=5, aliases={"yuki历史"}, block=True)


@scheduler.scheduled_job("cron", hour=config.reminder_time_hour, minute=config.reminder_time_minute, id="todaybefore_reminder")
async def todaybefore_reminder():
    bot = get_bot()
    data = await get_todaybefore()
    for i in groups:
        msg = f"「{nickname}·历史上的今天·定时」\n[CQ:at,qq={admin}]\n{data}"
        await bot.call_api('send_group_msg', **{'group_id': i, 'message': Message(msg)})


@todaybefore.handle()
async def todaybefore_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    data = await get_todaybefore()
    msg = f"「{nickname}·历史上的今天」\n[CQ:at,qq={event.get_user_id()}]\n{data}"
    await todaybefore.finish(Message(msg))
