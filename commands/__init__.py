import random
# from typing import O

import requests


def command_qod(bot, user, msg):
    response = requests.get("https://quotes.rest/qod?language=en", headers={"accept": "application/json"})
    if response.status_code == 200:
        data = response.json()
        msg = "Quote of the day: " + data['contents']['quotes'][0]['quote'] + " -" + data['contents']['quotes'][0]['author']
        bot.send_message(msg)


def command_cookie(bot, user, msg):
    cookie_quotes = (
        "C is for cookie, that's good enough for me",
        "Home is the place heart is. The heart where cookie is. Math clear: the home is a cookie.",
        "I’d give you a cookie, however, I ate it. ",
        "Me need cookie!",
        "Onion rings are simply vegetable doughnuts.",
        "I just took a DNA test - turns out 100% cookies… ",
    )
    bot.send_message(random.choice(cookie_quotes))


def command_blortbot(bot, user, msg):
    msg = "Blortbot knows stuff:"
    for key in COMMANDS.keys():
        msg += " =>  {}: {}".format(key, COMMANDS[key][1])
    msg += "  @blortbot for questions on the thing it knows."
    bot.send_message(msg)


def command_learn(bot, user, msg):
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

            if bot.corpus_name:
                bot.send_message("I know " + topic + " but I have forgotten " + bot.corpus_name)
            else:
                bot.send_message("I know " + topic)

            bot.corpus_name = topic
            bot.corpus_url = url
            bot.corpus_data = content.lower()

        bot.preprocess_corpus()


COMMANDS = {
    "!blortbot": (command_blortbot, "List all the magical things blortbot knows"),
    "!qod": (command_qod, "Quote of the day"),
    "!cookie": (command_cookie, "Get cookie monsters opinion"),
    "!learn": (command_learn, "Swap knowledge to new subject")
}
