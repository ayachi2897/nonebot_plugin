from nonebot import on_message
from nonebot.rule import keyword
from nonebot.adapters.onebot.v11 import Message,MessageEvent
import requests
import re
import textwrap


yydz = on_message(rule=keyword("星座运势"), priority=4, block=True)


@yydz.handle()
async def _(event: MessageEvent):
    
    appcode="48d70e8bc42740bc902d3f6a413bd26d"
    star = str(event.get_message()).strip()
    stars = star.replace("星座运势", "")
    stars = stars.replace("座", "")
    stars = stars.replace(" ", "")
    star = star.replace("星座运势", "")
    star = star.replace("座", "")
    star = star.replace(" ", "")
    star = star.replace("射手", "sheshou")
    star = star.replace("白羊", "baiyang")
    star = star.replace("金牛", "jinniu")
    star = star.replace("双子", "shuangzi")
    star = star.replace("巨蟹", "juxie")
    star = star.replace("狮子", "shizi")
    star = star.replace("处女", "chunv")
    star = star.replace("天秤", "tiancheng")
    star = star.replace("天蝎", "tianxie")
    star = star.replace("摩羯", "mojie")
    star = star.replace("水瓶", "shuiping")
    star = star.replace("双鱼", "shuangyu")
    req_data = {
        'needMonth':'0',
        'needTomorrow':'0',
        'needWeek':'0',
        'needYear':'0',
        'star':star
    }
    #修改结束
    url="https://ali-star-lucky.showapi.com/star"
    headers = {
        'Authorization':'APPCODE ' + appcode
    }
    html = requests.get(url, headers=headers,data=req_data)
    resp_body = html.json()["showapi_res_body"]["day"]
    try:  
        await yydz.send(await generate_content(resp_body, stars),at_sender=True)
    except:
        await yydz.send(message="星座运势获取错误了呢~")
    # try:
        # html = requests.get(url, headers=headers,data=req_data)
        # await yydz.send(html.text,at_sender=True)
    # except :
        # await yydz.send(message="URL错误")
    


async def generate_content(resp_body: dict, star: str):
    money_star = str(resp_body["money_star"])
    money_txt = "财富运势：" + str(resp_body["money_txt"])

    love_star = str(resp_body["love_star"])
    love_txt = "爱情运势：" + str(resp_body["love_txt"])
    grxz = str(resp_body["grxz"])

    work_star = str(resp_body["work_star"])
    work_txt = "工作运势：" + str(resp_body["work_txt"])

    summary_star = str(resp_body["summary_star"])
    general_txt = "运势简评：" + str(resp_body["general_txt"])

    lucky_num = str(resp_body["lucky_num"])
    lucky_time = str(resp_body["lucky_time"])
    lucky_color = str(resp_body["lucky_color"])
    lucky_direction = str(resp_body["lucky_direction"])

    day_notice = str(resp_body["day_notice"])

    time = str(resp_body["time"])

    yydz_answer = ""
    yydz_answer += "\n星座运势\n" + "星座：" + star + "座"
    yydz_answer += "\n日期：" + time

    yydz_answer += "\n"

    yydz_answer += "\n爱情指数：" + love_star + "\n"
    yydz_answer += textwrap.fill(love_txt, width=30)
    yydz_answer += "\n相配星座：" + grxz

    yydz_answer += "\n"

    yydz_answer += "\n工作指数：" + work_star + "\n"
    yydz_answer += textwrap.fill(work_txt, width=30)

    yydz_answer += "\n"

    yydz_answer += "\n财富指数：" + money_star + "\n"
    yydz_answer += textwrap.fill(money_txt, width=30)

    yydz_answer += "\n"

    yydz_answer += "\n综合指数：" + summary_star + "\n"
    yydz_answer += textwrap.fill(general_txt, width=30)

    yydz_answer += "\n"

    yydz_answer += "\n幸运数字：" + lucky_num
    yydz_answer += "\n幸运颜色：" + lucky_color
    yydz_answer += "\n幸运方位：" + lucky_direction
    yydz_answer += "\n幸运时间：" + lucky_time

    yydz_answer += "\n今日注意：" + day_notice
    yydz_answer += "\n"

    return yydz_answer

async def make_cache(stars, stars_cn):
    for i in range(0, 12):
        resp_body = (await get_data(stars[i]))["showapi_res_body"]["day"]
        content = await generate_content(resp_body, stars_cn[i])
