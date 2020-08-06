from typing import Dict, Callable, Tuple
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
