import base64
import io
from typing import List, Optional, Union, Callable
from PIL import Image
from nonebot import on_command
from .data_source import get_result
from .http_utils import AsyncHttpx
from utils.message_builder import image as image
import ujson as json
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Message
)
from nonebot.adapters.onebot.v11.message import MessageSegment
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger as logger_
from nonebot.log import default_format, default_filter

from nonebot.internal.params import Depends
from nonebot.internal.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageEvent




def get_message_text(data: Union[str, Message]) -> str:
    """
    说明:
        获取消息中 纯文本 的信息
    参数:
        :param data: event.json()
    """
    result = ""
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "text":
                result += msg["data"]["text"].strip() + " "
        return result.strip()
    else:
        for seg in data["text"]:
            result += seg.data["text"] + " "
    return result.strip()

def get_message_img(data: Union[str, Message]) -> List[str]:
    """
    说明:
        获取消息中所有的 图片 的链接
    参数:
        :param data: event.json()
    """
    img_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "image":
                img_list.append(msg["data"]["url"])
    else:
        for seg in data["image"]:
            img_list.append(seg.data["url"])
    return img_list

IMAGE_PATH = Path() / "data" / "qingxishu"

def image(
        file: Union[str, Path, bytes] = None,
        path: str = None,
        b64: str = None,
) -> Union[MessageSegment, str]:
    """
    说明:
        生成一个 MessageSegment.image 消息
        生成顺序：绝对路径(abspath) > base64(b64) > img_name
    参数:
        :param file: 图片文件名称，默认在 resource/img 目录下
        :param path: 图片所在路径，默认在 resource/img 目录下
        :param b64: 图片base64
    """
    if isinstance(file, Path):
        if file.exists():
            return MessageSegment.image(file)
        logger.warning(f"图片 {file.absolute()}缺失...")
        return ""
    elif isinstance(file, bytes):
        return MessageSegment.image(file)
    elif b64:
        return MessageSegment.image(b64 if "base64://" in b64 else "base64://" + b64)
    else:
        if file.startswith("http"):
            return MessageSegment.image(file)
        if len(file.split(".")) == 1:
            file += ".jpg"
        if (file := IMAGE_PATH / path / file if path else IMAGE_PATH / file).exists():
            return MessageSegment.image(file)
        else:
            logger.warning(f"图片 {file} 缺失...")
            return ""


async def _match(matcher: Matcher, event: MessageEvent, msg: Optional[str], func: Callable, contain_reply: bool):
    _list = func(event.message)
    if event.reply and contain_reply:
        _list = func(event.reply.message)
    if not _list and msg:
        await matcher.finish(msg)
    return _list




def ImageList(msg: Optional[str] = None, contain_reply: bool = True) -> List[str]:
    """
    说明:
        获取图片列表（包括回复时），含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
        :param contain_reply: 包含回复内容
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_img, contain_reply)

    return Depends(dependency)

def PlaintText(msg: Optional[str] = None, contain_reply: bool = True) -> str:
    """
    说明:
        获取纯文本且（包括回复时），含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
        :param contain_reply: 包含回复内容
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_text, contain_reply)

    return Depends(dependency)

LOG_PATH = Path() / "log"

logger = logger_


logger.add(
    LOG_PATH / f'{datetime.now().date()}.log',
    level='INFO',
    rotation='00:00',
    format=default_format,
    filter=default_filter,
    retention=timedelta(days=30))

logger.add(
    LOG_PATH / f'error_{datetime.now().date()}.log',
    level='ERROR',
    rotation='00:00',
    format=default_format,
    filter=default_filter,
    retention=timedelta(days=30))



__zx_plugin_name__ = "清晰术"
__plugin_usage__ = """
usage：
    清晰术[双/三四]重吟唱 [强力/中等/弱/不变/原]术式 [图片]
""".strip()
__plugin_des__ = "清晰术（又名图片超分术"
__plugin_cmd__ = ["清晰术[双/三四]重吟唱 [强力/中等/弱/不变/原]术式"]
__plugin_version__ = 0.1
__plugin_author__ = "hoshino 清晰术（hibikier改"
__plugin_settings__ = {
    "level": 5,
    "cmd": ["清晰术"],
}
__plugin_cd_limit__ = {}
__plugin_configs__ = {
    "API": {
        "value": None,
        "help": "参考 https://www.yuque.com/docs/share/bc837020-0261-4891-8da6-79979ece68c2#cf786ac0",
    },
}

thumbSize = (2500, 2500)

matcher = on_command("清晰术", priority=1, block=True)


@matcher.handle()
async def _(
    bot: Bot,
    event: MessageEvent,
    text: str = PlaintText(),
    img_list: List[str] = ImageList("你没有需要清晰术的图片！"),

):
    try:
        img = img_list[0]
        image_ = Image.open(io.BytesIO((await AsyncHttpx.get(img, timeout=20)).content))
        image_ = image_.convert("RGB")
        ix = image_.size[0]
        iy = image_.size[1]
        image_.thumbnail(thumbSize, resample=Image.ANTIALIAS)
        image_data = io.BytesIO()
        image_.save(image_data, format="JPEG")
        img = image_data.getvalue()
        i_b64 = "data:image/jpeg;base64," + base64.b64encode(img).decode()
        scale = 2
        con = "conservative"
        if "双重吟唱" in text:
            scale = 2
        elif "三重吟唱" in text and ix * iy < 400000:
            scale = 3
        elif "四重吟唱" in text and ix * iy < 400000:
            scale = 4
        if "强力术式" in text:
            con = "denoise3x"
        elif "中等术式" in text:
            con = "no-denoise"
            if scale == 2:
                con = "denoise2x"
        elif "弱术术式" in text:
            con = "no-denoise"
            if scale == 2:
                con = "denoise1x"
        elif "不变术式" in text:
            con = "no-denoise"
        elif "原术式" in text:
            con = "conservative"
        model_name = f"up{scale}x-latest-{con}.pth"
        await matcher.send(
            f"鸣大钟一次，推动杠杆，启动活塞和泵；鸣大钟两次，按下按钮，"
            f"发动机点火，点燃涡轮，注入生命；鸣大钟三次，齐声歌唱，赞美万机之神！大清晰术{con}{scale}重唱！",
            at_sender=True,
        )
        json_ = {"data": [i_b64, model_name, 2]}
        if result := await get_result(json_, api='https://hf.space/embed/baiyuhual/Real-CUGAN/+/api/predict/'):  # 然后进行超分辨率重建
            a = json.loads(result)
            a = "base64://" + a['data'][0].split("base64,")[1]
            await matcher.send(f"{scale}重唱{con}分支大清晰术！" + image(b64=a), at_sender=True)
        else:
            await matcher.send("清晰术失败", at_sender=True)
    except Exception as e:
        logger.error(f"超分发生错误 {type(e)}：{e}")
        await matcher.send("清晰术失败", at_sender=True)
