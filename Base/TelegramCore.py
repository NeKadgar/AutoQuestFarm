import random
import requests
import time


class TelegramCore:
    token = "1939263978:AAGqlT7pik7nMMar6FNRYRJWzQK0zH0XdXs"
    chat_id = 0
    url = "https://api.telegram.org/bot"

    @classmethod
    def setup(cls):
        message = str(random.randint(0, 999999))
        print("Please right now send \'{}\' to @WoWGrinder_bot".format(message))
        f = True
        while f:
            r = requests.get("{}{}/getUpdates".format(cls.url, cls.token))
            time.sleep(2)
            print(r.json())
            for m in r.json()["result"]:
                if m["message"]["text"] == message:
                    chat_id = m["message"]["chat"]["id"]
