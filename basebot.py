from typing import Tuple, Any
import socket
import os

ARE_YOU_ALIVE = "PING"
I_AM_ALIVE = "PONG"
ENCODING = "utf-8"
CHAT_MSG = "PRIVMSG"
COMMAND_TRIGGER = "!"


class BaseBot(object):
    def __init__(self, botname: str, token: str, channel: str, commands: dict):
        self.botname = botname
        self.token: str = token
        self.channel: str = channel
        self.commands = commands

        self.finished: bool = False
        self.server: Any = None

    def _handshake(self) -> None:
        # Note the bot name will not be what is specified here,
        # unless the Oauth token was generated for a Twitch Account with the same name.
        print(f"Connecting to #{self.channel} as {self.botname}")

        self.server.send(bytes("PASS " + self.token + "\r\n", ENCODING))
        self.server.send(bytes("NICK " + self.botname + "\r\n", ENCODING))
        self.server.send(bytes("JOIN " + f"#{self.channel}" + "\r\n", ENCODING))

    def _connect_to_twitch(self) -> None:
        connection_data = ("irc.chat.twitch.tv", 6667)
        self.server = socket.socket()
        self.server.connect(connection_data)
        self._handshake()

    def pong(self) -> None:
        self.server.sendall(bytes(I_AM_ALIVE + "\r\n", ENCODING))

    def send_message(self, msg: str) -> None:
        if self.server:
            self.server.send(
                bytes("PRIVMSG " + f"#{self.channel}" + " :(bot) " + msg + "\n", ENCODING)
            )
        else:
            print(f"No server connection: {msg}")

    def _is_command_msg(self, msg: str) -> bool:
        return msg[0] == COMMAND_TRIGGER and msg[1] != COMMAND_TRIGGER

    def process_base_msg(self, irc_response: str) -> None:
        if ARE_YOU_ALIVE in irc_response:
            self.pong()

        split_response = irc_response.split()

        if len(split_response) < 4:
            return

        user, msg = self._parse_user_and_msg(irc_response)
        if self._is_command_msg(msg):
            self.handle_command(user, msg)
        elif msg.startswith("@blortbot"):
            self.handle_direct_message(user, msg)
        else:
            print(f"{user}: {msg}")

    # TODO: refactor this sillyness
    def _parse_user_and_msg(self, irc_response) -> Tuple:
        user_info, _, _, *raw_msg = irc_response.split()
        raw_first_word, *raw_rest_of_the_message = raw_msg
        first_word = raw_first_word[1:]
        rest_of_the_message = " ".join(raw_rest_of_the_message)
        user = user_info.split("!")[0][1:]
        msg = f"{first_word} {rest_of_the_message}"
        return user, msg

    def handle_command(self, user, msg):
        command = msg.split(' ')
        if command[0] in self.commands.keys():
            print(f"Running command {msg} for {user}")
            self.commands[command[0]][0](self, user, msg)
        else:
            print(f"Unknown command: {msg} from {user}")

    def handle_direct_message(self, user, msg):
        print(f"{user}: {msg}")

    def run(self):
        self._connect_to_twitch()

        chat_buffer = ""
        socket.setdefaulttimeout(5)

        while not self.finished:
            chat_buffer = chat_buffer + self.server.recv(2048).decode("utf-8")
            if len(chat_buffer) > 0:
                messages = chat_buffer.split("\r\n")
                chat_buffer = messages.pop()

                for message in messages:
                    self.process_base_msg(message)
        print("Bot finished")


def command_hello(bot, user, msg):
    bot.send_message(f"Hello {user}")


if __name__ == "__main__":
    BOT_NAME = os.environ["BOT_NAME"]
    TOKEN = os.environ["TWITCH_OAUTH_TOKEN"]
    CHANNEL = os.environ["CHANNEL"]

    COMMANDS = {
        "!hello": (command_hello, "Sample command"),
    }

    tb = BaseBot(BOT_NAME, TOKEN, CHANNEL, COMMANDS)
    tb.process_base_msg("1user 2b 3c -!hello")
    tb.run()
