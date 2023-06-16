from typing import Dict, Union, Optional, List, Any, Literal
from .user_agent import get_user_agent


from pathlib import Path
from httpx import Response
from asyncio.exceptions import TimeoutError
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.message import MessageSegment
from playwright.async_api import Page, BrowserContext
from httpx import ConnectTimeout
from retrying import retry
import asyncio
import aiofiles
import httpx
import rich

from datetime import datetime, timedelta
from loguru import logger as logger_
from nonebot.log import default_format, default_filter
import io
from playwright.async_api import Browser

async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)


def install():
    """自动安装、更新 Chromium"""
    logger.info("正在检查 Chromium 更新")
    import sys
    from playwright.__main__ import main

    sys.argv = ["", "install", "chromium"]
    try:
        main()
    except SystemExit:
        pass

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
    elif isinstance(file, (bytes, io.BytesIO)):
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

SYSTEM_PROXY: Optional[str] = None  # 全局代理

def get_local_proxy():
    """
    说明:
        获取 config.py 中设置的代理
    """
    return SYSTEM_PROXY if SYSTEM_PROXY else None


class AsyncHttpx:

    proxy = {"http://": get_local_proxy(), "https://": get_local_proxy()}

    @classmethod
    @retry(stop_max_attempt_number=3)
    async def get(
        cls,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        verify: bool = True,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> Response:
        """
        说明:
            Get
        参数:
            :param url: url
            :param params: params
            :param headers: 请求头
            :param cookies: cookies
            :param verify: verify
            :param use_proxy: 使用默认代理
            :param proxy: 指定代理
            :param timeout: 超时时间
        """
        if not headers:
            headers = get_user_agent()
        proxy = proxy if proxy else cls.proxy if use_proxy else None
        async with httpx.AsyncClient(proxies=proxy, verify=verify) as client:
            return await client.get(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                **kwargs
            )

    @classmethod
    async def post(
        cls,
        url: str,
        *,
        data: Optional[Dict[str, str]] = None,
        content: Any = None,
        files: Any = None,
        verify: bool = True,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        json: Optional[Dict[str, Union[Any]]] = None,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> Response:
        """
        说明:
            Post
        参数:
            :param url: url
            :param data: data
            :param content: content
            :param files: files
            :param use_proxy: 是否默认代理
            :param proxy: 指定代理
            :param json: json
            :param params: params
            :param headers: 请求头
            :param cookies: cookies
            :param timeout: 超时时间
        """
        if not headers:
            headers = get_user_agent()
        proxy = proxy if proxy else cls.proxy if use_proxy else None
        async with httpx.AsyncClient(proxies=proxy, verify=verify) as client:
            return await client.post(
                url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                **kwargs,
            )

    @classmethod
    async def download_file(
        cls,
        url: str,
        path: Union[str, Path],
        *,
        params: Optional[Dict[str, str]] = None,
        verify: bool = True,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 30,
        stream: bool = False,
        **kwargs,
    ) -> bool:
        """
        说明:
            下载文件
        参数:
            :param url: url
            :param path: 存储路径
            :param params: params
            :param verify: verify
            :param use_proxy: 使用代理
            :param proxy: 指定代理
            :param headers: 请求头
            :param cookies: cookies
            :param timeout: 超时时间
            :param stream: 是否使用流式下载（流式写入+进度条，适用于下载大文件）
        """
        if isinstance(path, str):
            path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            for _ in range(3):
                if not stream:
                    try:
                        content = (
                            await cls.get(
                                url,
                                params=params,
                                headers=headers,
                                cookies=cookies,
                                use_proxy=use_proxy,
                                proxy=proxy,
                                timeout=timeout,
                                **kwargs,
                            )
                        ).content
                        async with aiofiles.open(path, "wb") as wf:
                            await wf.write(content)
                            logger.info(f"下载 {url} 成功.. Path：{path.absolute()}")
                        return True
                    except (TimeoutError, ConnectTimeout):
                        pass
                else:
                    if not headers:
                        headers = get_user_agent()
                    proxy = proxy if proxy else cls.proxy if use_proxy else None
                    try:
                        async with httpx.AsyncClient(proxies=proxy, verify=verify) as client:
                            async with client.stream(
                                "GET",
                                url,
                                params=params,
                                headers=headers,
                                cookies=cookies,
                                timeout=timeout,
                                **kwargs
                            ) as response:
                                logger.info(f"开始下载 {path.name}.. Path: {path.absolute()}")
                                async with aiofiles.open(path, "wb") as wf:
                                    total = int(response.headers["Content-Length"])
                                    with rich.progress.Progress(
                                        rich.progress.TextColumn(path.name),
                                        "[progress.percentage]{task.percentage:>3.0f}%",
                                        rich.progress.BarColumn(bar_width=None),
                                        rich.progress.DownloadColumn(),
                                        rich.progress.TransferSpeedColumn()
                                    ) as progress:
                                        download_task = progress.add_task("Download", total=total)
                                        async for chunk in response.aiter_bytes():
                                            await wf.write(chunk)
                                            await wf.flush()
                                            progress.update(download_task, completed=response.num_bytes_downloaded)
                                    logger.info(f"下载 {url} 成功.. Path：{path.absolute()}")
                        return True
                    except (TimeoutError, ConnectTimeout):
                        pass
            else:
                logger.error(f"下载 {url} 下载超时.. Path：{path.absolute()}")
        except Exception as e:
            logger.error(f"下载 {url} 未知错误 {type(e)}：{e}.. Path：{path.absolute()}")
        return False

    @classmethod
    async def gather_download_file(
        cls,
        url_list: List[str],
        path_list: List[Union[str, Path]],
        *,
        limit_async_number: Optional[int] = None,
        params: Optional[Dict[str, str]] = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> List[bool]:
        """
        说明:
            分组同时下载文件
        参数:
            :param url_list: url列表
            :param path_list: 存储路径列表
            :param limit_async_number: 限制同时请求数量
            :param params: params
            :param use_proxy: 使用代理
            :param proxy: 指定代理
            :param headers: 请求头
            :param cookies: cookies
            :param timeout: 超时时间
        """
        if n := len(url_list) != len(path_list):
            raise UrlPathNumberNotEqual(
                f"Url数量与Path数量不对等，Url：{len(url_list)}，Path：{len(path_list)}"
            )
        if limit_async_number and n > limit_async_number:
            m = float(n) / limit_async_number
            x = 0
            j = limit_async_number
            _split_url_list = []
            _split_path_list = []
            for _ in range(int(m)):
                _split_url_list.append(url_list[x:j])
                _split_path_list.append(path_list[x:j])
                x += limit_async_number
                j += limit_async_number
            if int(m) < m:
                _split_url_list.append(url_list[j:])
                _split_path_list.append(path_list[j:])
        else:
            _split_url_list = [url_list]
            _split_path_list = [path_list]
        tasks = []
        result_ = []
        for x, y in zip(_split_url_list, _split_path_list):
            for url, path in zip(x, y):
                tasks.append(
                    asyncio.create_task(
                        cls.download_file(
                            url,
                            path,
                            params=params,
                            headers=headers,
                            cookies=cookies,
                            use_proxy=use_proxy,
                            timeout=timeout,
                            proxy=proxy,
                            ** kwargs,
                        )
                    )
                )
            _x = await asyncio.gather(*tasks)
            result_ = result_ + list(_x)
            tasks.clear()
        return result_


class AsyncPlaywright:

    @classmethod
    async def _new_page(cls, user_agent: Optional[str] = None, **kwargs) -> Page:
        """
        说明:
            获取一个新页面
        参数:
            :param user_agent: 请求头
        """
        browser = await get_browser()
        if browser:
            return await browser.new_page(user_agent=user_agent, **kwargs)
        raise BrowserIsNone("获取Browser失败...")

    @classmethod
    async def new_context(cls, user_agent: Optional[str] = None, **kwargs) -> BrowserContext:
        """
        说明:
            获取一个新上下文
        参数:
            :param user_agent: 请求头
        """
        browser = await get_browser()
        if browser:
            return await browser.new_context(user_agent=user_agent, **kwargs)
        raise BrowserIsNone("获取Browser失败...")

    @classmethod
    async def goto(
        cls,
        url: str,
        *,
        timeout: Optional[float] = 100000,
        wait_until: Optional[
            Literal["domcontentloaded", "load", "networkidle"]
        ] = "networkidle",
        referer: str = None,
        **kwargs
    ) -> Optional[Page]:
        """
        说明:
            goto
        参数:
            :param url: 网址
            :param timeout: 超时限制
            :param wait_until: 等待类型
            :param referer:
        """
        page = None
        try:
            page = await cls._new_page(**kwargs)
            await page.goto(url, timeout=timeout, wait_until=wait_until, referer=referer)
            return page
        except Exception as e:
            logger.warning(f"Playwright 访问 url：{url} 发生错误 {type(e)}：{e}")
            if page:
                await page.close()
        return None

    @classmethod
    async def screenshot(
        cls,
        url: str,
        path: Union[Path, str],
        element: Union[str, List[str]],
        *,
        wait_time: Optional[int] = None,
        viewport_size: Dict[str, int] = None,
        wait_until: Optional[
            Literal["domcontentloaded", "load", "networkidle"]
        ] = "networkidle",
        timeout: float = None,
        type_: Literal["jpeg", "png"] = None,
        **kwargs
    ) -> Optional[MessageSegment]:
        """
        说明:
            截图，该方法仅用于简单快捷截图，复杂截图请操作 page
        参数:
            :param url: 网址
            :param path: 存储路径
            :param element: 元素选择
            :param wait_time: 等待截取超时时间
            :param viewport_size: 窗口大小
            :param wait_until: 等待类型
            :param timeout: 超时限制
            :param type_: 保存类型
        """
        page = None
        if viewport_size is None:
            viewport_size = dict(width=2560, height=1080)
        if isinstance(path, str):
            path = Path(path)
        try:
            page = await cls.goto(url, wait_until=wait_until, **kwargs)
            await page.set_viewport_size(viewport_size)
            if isinstance(element, str):
                if wait_time:
                    card = await page.wait_for_selector(element, timeout=wait_time * 1000)
                else:
                    card = await page.query_selector(element)
            else:
                card = page
                for e in element:
                    if wait_time:
                        card = await card.wait_for_selector(e, timeout=wait_time * 1000)
                    else:
                        card = await card.query_selector(e)
            await card.screenshot(path=path, timeout=timeout, type=type_)
            return image(path)
        except Exception as e:
            logger.warning(f"Playwright 截图 url：{url} element：{element} 发生错误 {type(e)}：{e}")
        finally:
            if page:
                await page.close()
        return None


class UrlPathNumberNotEqual(Exception):
    pass


class BrowserIsNone(Exception):
    pass
