# blortbot project
Twitchbot which implements natural landuage processing with wikipedia pages as corpus

Comes with 2 bots:

## BaseBot
An extensible bot which recognises !hello messages and responds with hello {user}.

Uses only standard library so no need to install dependencies

To run you need to set 3 environment variables:
 - BOT_NAME
 - TOKEN
 - CHANNEL

Then run:
```
python basebot.py
```

To add commands you can add to COMMANDS dictionary:
```python
    COMMANDS = {
        "!hello": (command_hello, "Sample command"),
    }
```

## BlortBot
Extends BaseBot by overriding handle_direct_message and adding more commands:
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

BlortBot uses natural language processing and cosine similarity to respond with a vaguely intellegible answer.

More info:
https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity

