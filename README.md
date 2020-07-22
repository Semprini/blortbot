# blortbot project
Twitchbot which implements natural landuage processing with wikipedia pages as corpus

## Docker
docker build -t blortbot .
docker run -e TWITCH_OAUTH_TOKEN='your token heere' --name blortbot_1 blortbot

You can also override these environment variables using more -e args when running:
- BOT_NAME (default = blortbot)
- CHANNEL (default = beginbot)


Code has 2 bots:


## BlortBot
Extends BaseBot (see below) by overriding handle_direct_message and adding more commands:
 - !blortbot: List all the magical things blortbot knows
 - !qod: Quote of the day grabbed from quotes.rest
 - !cookie: Get cookie monsters opinion
 - !learn: Swap knowledge to new subject

Once a subject has been learned then you can message @blortbot to get answers. 

For Example in twitch chat:
```
 > !learn kung fu
blortbot: I know kung fu
 > @blortbot who was bruce lee's teacher
blortbot: yip man was the teacher of [[bruce lee]].
```
![kung fu](https://raw.githubusercontent.com/Semprini/blortbot/master/kungfu.png)

BlortBot does have dependencies so use:

```pip install -r requirements.txt```

And needs an environment variable:
 
 - TWITCH_OAUTH_TOKEN # Get the value for this here: https://twitchapps.com/tmi/

BlortBot uses natural language processing and cosine similarity to respond with a vaguely intellegible answer.

More info:
https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity

## BaseBot
An extensible bot which recognises !hello messages and responds with hello {user}. Oo'd from https://gitlab.com/beginbot/python_twitch_bot_no_deps

Uses only standard library so no need to install dependencies

To run you need to set 3 environment variables:
 - BOT_NAME
 - TOKEN
 - CHANNEL

Then run:
```
python basebot.py
```

To add commands you annotate a function with the command decorator:
```python
@command('hello', 'responds with hello')
def command_hello(bot, user, msg):
    ...
```

