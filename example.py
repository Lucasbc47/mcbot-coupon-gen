import json
import os

from selenium.webdriver.chrome.service import Service
from bot.mcbot import MCBot

with open('config.json', 'r') as file:
    config = json.load(file)

bot = MCBot(
    hidden=config["esconder_webdriver"],
    country=config["country"],
    cnpj_mc=config["cnpj_mc_donalds"],
    quantia=config["quantia"]
)

if os.name == 'posix': ## for linux
    bot.executable_path=config["diretorio_webdriver"]
if os.name == "nt": ## correction for windows
    bot.service = Service(config["diretorio_webdriver"])

bot.start_gen()
