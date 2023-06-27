import json
from bot.mcbot import MCBot

with open('config.json', 'r') as file:
    config = json.load(file)

bot = MCBot(
    executable_path=config["diretorio_webdriver"],
    hidden=config["esconder_webdriver"],
    country=config["country"],
    cnpj_mc=config["cnpj_mc_donalds"],
    quantia=config["quantia"]
)

bot.start_gen()