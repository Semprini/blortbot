import requests
import random
from typing import Any, Optional

from .. import command


@command("qod", "Quote of the day")
def command_qod(bot: Any, user: str, msg: str) -> Optional[str]:
    response = requests.get("https://quotes.rest/qod?language=en", headers={"accept": "application/json"})
    if response.status_code == 200:
        data = response.json()
        msg = "Quote of the day: " + data['contents']['quotes'][0]['quote'] + " -" + data['contents']['quotes'][0]['author']
        bot.send_message(msg)
        return msg
    return None


@command('cookie', 'Get cookie monsters opinion')
def command_cookie(bot: Any, user: str, msg: str) -> str:
    cookie_quotes = (
        "C is for cookie, that's good enough for me",
        "Home is the place heart is. The heart where cookie is. Math clear: the home is a cookie.",
        "I’d give you a cookie, however, I ate it. ",
        "Me need cookie!",
        "Onion rings are simply vegetable doughnuts.",
        "I just took a DNA test - turns out 100% cookies… ",
    )
    msg = random.choice(cookie_quotes)
    bot.send_message(msg)
    return msg
