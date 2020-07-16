import random
from typing import Any

import requests

from blortbot import Corpus
from basebot import command, COMMANDS


@command("qod", "Quote of the day")
def command_qod(bot: Any, user: str, msg: str) -> None:
    response = requests.get("https://quotes.rest/qod?language=en", headers={"accept": "application/json"})
    if response.status_code == 200:
        data = response.json()
        msg = "Quote of the day: " + data['contents']['quotes'][0]['quote'] + " -" + data['contents']['quotes'][0]['author']
        bot.send_message(msg)


@command('cookie', 'Get cookie monsters opinion')
def command_cookie(bot: Any, user: str, msg: str) -> None:
    cookie_quotes = (
        "C is for cookie, that's good enough for me",
        "Home is the place heart is. The heart where cookie is. Math clear: the home is a cookie.",
        "I’d give you a cookie, however, I ate it. ",
        "Me need cookie!",
        "Onion rings are simply vegetable doughnuts.",
        "I just took a DNA test - turns out 100% cookies… ",
    )
    bot.send_message(random.choice(cookie_quotes))


@command('blortbot', 'List all the magical things blortbot can do')
def command_blortbot(bot: Any, user: str, msg: str) -> None:
    msg = "Blortbot knows stuff:"
    for key in COMMANDS.keys():
        msg += " =>  {}: {}".format(key, COMMANDS[key][1])
    msg += "  @blortbot for questions on the thing it knows."
    bot.send_message(msg)


@command('learn', 'Swap knowledge to new subject')
def command_learn(bot: Any, user: str, msg: str) -> None:
    # Skip the !learn command and get the topic
    topic = msg[7:]
    if len(topic) < 3:
        return

    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={topic}&limit=1&namespace=0&format=json"
    response = requests.get(url, headers={"accept": "application/json"})
    if response.status_code == 200:
        data = response.json()
        if len(data[1]) == 0:
            bot.send_message("Sorry, " + topic + " bores me.")
            return
        page = data[1][0]

        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={page}&rvslots=*&rvprop=content&formatversion=2&format=json"
        response = requests.get(url, headers={"accept": "application/json"})
        if response.status_code == 200:
            data = response.json()

            content = data["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
            if content.lower().startswith("#redirect"):
                page = content[9:].replace("[[", "").replace("]]", "").split('\n')[0].strip()

                url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={page}&rvslots=*&rvprop=content&formatversion=2&format=json"
                response = requests.get(url, headers={"accept": "application/json"})
                data = response.json()
                content = data["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]

            bot.corpus = Corpus(topic, url, content)
