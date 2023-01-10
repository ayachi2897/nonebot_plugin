from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message
import requests
import os
import json

stream_sub = on_command("直播间订阅")

@stream_sub.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).lstrip()
    args = args.replace("直播间订阅", "")
    args = args.replace(" ", "")
    args = args.replace("UID", "")
    args = args.replace(":", "")
    print(args)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
        #"Cookie": "_uuid=A84EE9DB-6F1E-23A9-6143-C12F0452F1AA09526infoc; buvid3=C2001EF8-B63F-4BFE-A82F-B874767350BE138387infoc; CURRENT_FNVAL=80; bxlackside_state=1; rpdid=|(u)Yl|YummR0J'uYuY|lYml|; fingerprint=7bfed0535c2f297ab55b045f06a84e24; buvid_fp=C2001EF8-B63F-4BFE-A82F-B874767350BE138387infoc; buvid_fp_plain=C2001EF8-B63F-4BFE-A82F-B874767350BE138387infoc; SESSDATA=43a18e0d%2C1634741154%2C55936%2A41; bili_jct=2de33df16746e3f118d41a384666c344; DedeUserID=36409264; DedeUserID__ckMd5=89cb10047d92a5b5; sid=anjfrwb7; LIVE_BUVID=AUTO6616204776752283; bp_video_offset_36409264=537582347573076463; CURRENT_QUALITY=80; bsource=search_bing; _dfcaptcha=4fed6d52ff72669b763551d36f761d20; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1624547492,1624547545,1624547563,1624796501; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1624796501; PVID=14",
        "Cookie": "buvid3=5BCF632D-B4F7-4F04-A27D-5D3F359380FE148801infoc; LIVE_BUVID=AUTO2516337128046552; buvid_fp_plain=undefined; buvid4=DEA62F84-FAA3-00C4-3716-A8CB4A3D9BC009839-022012507-mHWJTrTCDEK9rKolWxBkfA%3D%3D; fingerprint3=6743fca14ed5e71141f2a38ccd392c3a; DedeUserID=11701289; DedeUserID__ckMd5=1fecde28b625caf7; nostalgia_conf=-1; hit-dyn-v2=1; go_old_video=1; CURRENT_BLACKGAP=0; blackside_state=0; PEA_AU=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJiaWQiOjExNzAxMjg5LCJwaWQiOjkzMzg5NywiZXhwIjoxNjg2ODA4MjQ1LCJpc3MiOiJ0ZXN0In0.dK97r45GJCQGAja35LIabAJ1n3ALOuuFlWRw5KHi6CU; CURRENT_QUALITY=80; b_timer=%7B%22ffp%22%3A%7B%22666.4.fp.risk_5BCF632D%22%3A%22181F92F0823%22%2C%22444.41.fp.risk_5BCF632D%22%3A%22182D43C9D2F%22%2C%22333.788.fp.risk_5BCF632D%22%3A%22182D35569FF%22%2C%22888.2421.fp.risk_5BCF632D%22%3A%22182CF98385E%22%2C%22444.8.fp.risk_5BCF632D%22%3A%22182D43CB6D6%22%2C%22333.337.fp.risk_5BCF632D%22%3A%22182A8E5B4A1%22%2C%22777.5.0.0.fp.risk_5BCF632D%22%3A%22182C3029B6B%22%2C%22333.976.fp.risk_5BCF632D%22%3A%221824BB23B65%22%2C%22333.999.fp.risk_5BCF632D%22%3A%22182D43E4293%22%2C%22333.880.fp.risk_5BCF632D%22%3A%22182A867936D%22%2C%22444.42.fp.risk_5BCF632D%22%3A%221829D673945%22%2C%22444.62.fp.risk_5BCF632D%22%3A%22182A2740468%22%2C%22333.1193.fp.risk_5BCF632D%22%3A%22182D35570C3%22%2C%22444.55.fp.risk_5BCF632D%22%3A%22182785DAA6F%22%2C%22444.45.fp.risk_5BCF632D%22%3A%221827DA6DB83%22%2C%22333.851.fp.risk_5BCF632D%22%3A%2218282E0BDB4%22%2C%22333.52.fp.risk_5BCF632D%22%3A%22182A27A1297%22%2C%22333.997.fp.risk_5BCF632D%22%3A%22182A27A27CD%22%2C%22888.14.fp.risk_5BCF632D%22%3A%22182A27AF859%22%2C%22333.794.fp.risk_5BCF632D%22%3A%22182A27B4F58%22%7D%7D; b_nut=100; _uuid=4A98B10102-DF37-27DE-FE7D-7D27D291054C714527infoc; hit-new-style-dyn=0; i-wanna-go-feeds=-1; rpdid=|(J|)YJ|)ku|0J'uYYmJRmYu); CURRENT_FNVAL=4048; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1671295296; b_ut=5; fingerprint=f8b3ee8fd9c63d9e34e5cdf35e24949c; i-wanna-go-back=2; share_source_origin=QQ; bp_video_offset_11701289=748335027180273700; bsource=share_source_qqchat; SESSDATA=a6a77d7d%2C1688829225%2C40340%2A12; bili_jct=3eda325d5608c4be92074b1c78f71d3f; sid=6fw2n67o; _dfcaptcha=0fdd9b628322a73c1036efe49b89443b; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1673277259; innersign=0; b_lsid=71DEBC61_1859743257E; buvid_fp=f8b3ee8fd9c63d9e34e5cdf35e24949c; PVID=3",
        "Content-Type": "application/json;charset=utf-8"
    }
    url="https://api.bilibili.com/x/space/acc/info?mid="
    url=url + args
    args_api = requests.get(url, headers=header)
    args_api.encoding='utf-8'
    args_api = args_api.text
    args_api = json.loads(args_api)
    args_api = args_api["data"]["live_room"]
    print(args_api)
    if args_api == None:
        args = ""
    if args:
        state["sentence"] = args

@stream_sub.got("sentence", prompt="订阅哪个用户的直播间? 请输入用户UID! (只支持哔哩哔哩订阅)")
async def handle_city(bot: Bot, event: Event, state: T_State):
    sentence = state["sentence"]
    file = "/Users/28972/bot1/src/plugins/nonebot_bilibili_stream_sub/resource/sub.json"

    if "http" in sentence or "https" in sentence:
        split_last = sentence.split("/")
        if split_last[-2] == "":
            sentence = split_last[-3]
        else:
            sentence = split_last[-2]

    sub_data = {
        "sub_user_id": sentence,
        "sub_user": str(event.get_user_id()),
        "sub_group": str(event.group_id),
        "live_status": False,
        "live_info": False
    }

    if open(file, "r", encoding="utf8").read() == "":
        file_data = {
            "sub": [{
                "sub_user_id": sentence,
                "sub_user": str(event.get_user_id()),
                "sub_group": str(event.group_id),
                "live_status": False,
                "live_info": False
            }]
        }
        open(file, "wb+").write(json.dumps(file_data).encode())
    else:
        file_data = json.load(open(file, "r"))

        flag = False
        for data in file_data["sub"]:
            if data["sub_user_id"] == sentence and data["sub_group"] == str(event.group_id):
                await stream_sub.send(Message("此群聊中已经订阅了哔哩哔哩用户ID为 {} 的直播间了!".format(sentence)))
                flag = True

        if flag == False:
            file_data["sub"].append(sub_data)
            open(file, "w").write(json.dumps(file_data))
            await stream_sub.send(Message("订阅成功!"))
