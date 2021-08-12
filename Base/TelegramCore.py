import random
import requests
import time
import json

class TelegramCore:
    token = "1939263978:AAGqlT7pik7nMMar6FNRYRJWzQK0zH0XdXs"
    chat_id = 0
    bin_dict = {}
    url = "https://api.telegram.org/bot"

    @classmethod
    def load(cls):
        with open("bin") as file:
            cls.bin_dict = json.load(file)
            print(cls.bin_dict)
            cls.chat_id = cls.bin_dict["chat_id"]

    @classmethod
    def setup(cls, session_name):
        cls.load()
        if cls.chat_id == 0:
            message = str(random.randint(0, 999999))
            print("Please right now send \'{}\' to @WoWGrinder_bot".format(message))
            f = True
            while f:
                r = requests.get("{}{}/getUpdates".format(cls.url, cls.token))
                time.sleep(2)
                for m in r.json()["result"]:
                    if m["message"]["text"] == message:
                        cls.chat_id = m["message"]["chat"]["id"]
                        cls.bin_dict["chat_id"] = cls.chat_id
                        with open('bin', 'w') as file:
                            print(cls.bin_dict)
                            json.dump(cls.bin_dict, file)
                        f = False
            cls.send_message(session_name, "Setup completed!")


    @classmethod
    def send_message(cls, session, message):
        message = "Session {}:\n{}".format(str(session), str(message))
        r = requests.get("{}{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}".format(
                        cls.url, cls.token, cls.chat_id, message))
