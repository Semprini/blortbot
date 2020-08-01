import random
import requests
from typing import Any, Optional, Dict, Callable, Tuple
import functools

from basebot import COMMAND_TRIGGER

COMMANDS: Dict[str, Tuple[Callable, str]] = {}


def command(name, desc):
    @functools.wraps(name, desc)
    def wrapper(func):
        """Register a function as a command"""
        COMMANDS[COMMAND_TRIGGER + name] = (func, desc)
        return func
    return wrapper


@command('helloblort', 'responds with hello')
def command_hello(bot, user, msg):
    output = f"Hello {user}"
    bot.send_message(output)
    return output


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


@command('blortbot', 'List all the magical things blortbot can do')
def command_blortbot(bot: Any, user: str, msg: str) -> str:
    msg = "Blortbot knows stuff:"
    for key in COMMANDS.keys():
        msg += " =>  {}: {}".format(key, COMMANDS[key][1])
    msg += "  @blortbot for questions on the thing it knows."
    bot.send_message(msg)
    return msg
