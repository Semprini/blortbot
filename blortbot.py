"""
    Using nltk to do a chatbot which uses wikipedia pages

    Using this article for reference and code
    https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e
"""
import os
import string
import warnings
from typing import Optional

import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from basebot import BaseBot

# Ignore the warnings from sklearn\feature_extraction
warnings.filterwarnings('ignore')


class Corpus():
    def __init__(self, topic, url, content):
        self.topic = topic
        self.url = url
        self.content = content.lower()
        self.sent_tokens = None
        self.word_tokens = None

        self._lemmer = WordNetLemmatizer()
        self._remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

        self.preprocess()

    def preprocess(self):
        # converts to list of sentences
        self.sent_tokens = nltk.sent_tokenize(self.content)
        # converts to list of words
        self.word_tokens = nltk.word_tokenize(self.content)

    def LemTokens(self, tokens):
        return [self._lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self._remove_punct_dict)))


class BlortBot(BaseBot):
    def __init__(self, botname: str, token: str, channel: str, commands: Optional[dict] = None):
        super().__init__(botname, token, channel, commands)

        nltk.download('popular', quiet=True)

        self._corpus = None

    def handle_direct_message(self, usr, msg):
        question = msg.strip(f"@{self.botname} ")
        response = self.response(question).replace("\n", "|")[:350]
        print(f"Answering {question} with: {response}")
        self.send_message(response)

    def response(self, user_response):
        robo_response = ''
        self.corpus.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.corpus.LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.corpus.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf == 0):
            robo_response = "I'm sorry! I don't understand you"
        else:
            robo_response = self.corpus.sent_tokens[idx]
        self.corpus.sent_tokens.remove(user_response)

        # Remove references
        secondDelPos = 0
        while secondDelPos != -1:
            firstDelPos = robo_response.find("<ref>")
            secondDelPos = robo_response.find("</ref>", firstDelPos)
            if firstDelPos != -1:
                if secondDelPos == -1:
                    robo_response = robo_response.replace(robo_response[firstDelPos:], "")
                else:
                    robo_response = robo_response.replace(robo_response[firstDelPos: secondDelPos + 6], "")

        return robo_response

    @property
    def corpus(self):
        return self._corpus

    @corpus.setter
    def corpus(self, corpus):
        if self._corpus is not None:
            self.send_message("I know " + corpus.topic + " but I have forgotten " + self._corpus.topic)
        else:
            self.send_message("I know " + corpus.topic)

        self._corpus = corpus


if __name__ == "__main__":
    # Get the value for this here: https://twitchapps.com/tmi/
    TOKEN = os.environ["TWITCH_OAUTH_TOKEN"]

    import commands as command_set  # noqa: F401
    bb = BlortBot("blortbot", TOKEN, "beginbot")
    bb.run()
