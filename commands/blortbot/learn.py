from typing import Any, Optional
import requests

from blortbot import Corpus
from .. import command


@command('learn', 'Swap knowledge to new subject')
def command_learn(bot: Any, user: str, msg: str) -> Optional[str]:
    # Skip the !learn command and get the topic
    topic = msg[7:]
    if len(topic) < 3:
        return None

    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={topic}&limit=1&namespace=0&format=json"
    response = requests.get(url, headers={"accept": "application/json"})
    if response.status_code == 200:
        data = response.json()
        if len(data[1]) == 0:
            msg = "Sorry, " + topic + " bores me."
            bot.send_message(msg)
            return msg
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
            return "Learnt" + topic
    return None
