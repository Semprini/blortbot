from typing import Any

from .. import command, COMMANDS


@command('helloblort', 'responds with hello')
def command_hello(bot, user, msg):
    output = f"Hello {user}"
    bot.send_message(output)
    return output


@command('blortbot', 'List all the magical things blortbot can do')
def command_blortbot(bot: Any, user: str, msg: str) -> str:
    msg = "Blortbot knows stuff:"
    for key in COMMANDS.keys():
        msg += " =>  {}: {}".format(key, COMMANDS[key][1])
    msg += "  @blortbot for questions on the thing it knows."
    bot.send_message(msg)
    return msg
