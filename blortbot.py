"""
    Using nltk to do a chatbot which uses wikipedia pages

    Using this article for reference and code
    https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e
"""
import os
import string
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

from basebot import BaseBot
from commands import COMMANDS


warnings.filterwarnings('ignore')


class BlortBot(BaseBot):
    def __init__(self, botname: str, token: str, channel: str, commands: dict):
        super().__init__(botname, token, channel, commands)

        nltk.download('popular', quiet=True)

        self.corpus_name = None
        self.corpus_url = None
        self.corpus_data = None
        self.sent_tokens = None
        self.word_tokens = None

        self.lemmer = WordNetLemmatizer()
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def handle_direct_message(self, usr, msg):
        question = msg.strip(f"@{self.botname}").strip()
        response = self.response(question).replace("\n", "|")[:350]
        print(f"Answering {question} with {response}")
        self.send_message(response)

    def preprocess_corpus(self):
        # converts to list of sentences
        self.sent_tokens = nltk.sent_tokenize(self.corpus_data)
        # converts to list of words
        self.word_tokens = nltk.word_tokenize(self.corpus_data)

    def response(self, user_response):
        robo_response = ''
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf == 0):
            robo_response = "I'm sorry! I don't understand you"
        else:
            robo_response = self.sent_tokens[idx]
        self.sent_tokens.remove(user_response)

        secondDelPos = 0
        while secondDelPos != -1:
            firstDelPos = robo_response.find("<ref>", secondDelPos)
            secondDelPos = robo_response.find("</ref>", firstDelPos)
            if firstDelPos != -1 and secondDelPos != -1:
                robo_response = robo_response.replace(robo_response[firstDelPos: secondDelPos + 6], "")

        return robo_response


if __name__ == "__main__":
    # Get the value for this here: https://twitchapps.com/tmi/
    TOKEN = os.environ["TWITCH_OAUTH_TOKEN"]

    bb = BlortBot("blortbot", TOKEN, "blortbot", COMMANDS)
    bb.run()
