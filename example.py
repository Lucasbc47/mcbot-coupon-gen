import json
import os
from selenium.webdriver.chrome.service import Service
from bot.mcbot import MCBot

with open('config.json', 'r') as file:
    config = json.load(file)

if os.name == 'nt':  # Windows
    service = Service(executable_path=config["diretorio_webdriver"])
else:  # Linux/Mac
    service = Service(executable_path=config["diretorio_webdriver"])

bot = MCBot(
    service=service,
    hidden=config["esconder_webdriver"],
    country=config["country"],
    cnpj_mc=config["cnpj_mc_donalds"],
    quantia=config["quantia"]
)

bot.start_gen()
