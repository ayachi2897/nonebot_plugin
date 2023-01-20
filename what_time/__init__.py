from nonebot import on_message
from nonebot.rule import fullmatch
from nonebot.adapters.onebot.v11 import Message
import requests




        
what_time = on_message(rule=fullmatch({"几点了","现在几点"}), priority=4, block=True)
@what_time.handle()
async def _():
    time_url= "https://api.guyunge.top/API/time.php"
    response = requests.get(time_url)
    response.encoding='utf-8'
    html = response.text
    await what_time.send(Message(html))
    
    
    
