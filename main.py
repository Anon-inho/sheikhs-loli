import interactions
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = interactions.Client(
    token=str(DISCORD_TOKEN),
    intents=interactions.Intents.ALL)

bot.load("scheduling")
bot.load("confirm")
bot.load("buttons")
bot.load("tickets")
bot.load("inrole")
bot.load("result")
bot.load("embed")
bot.load("create")
bot.load("randomfile")
bot.load("roles")
bot.load("request")
# bot.load("docs")

@bot.event
async def on_ready():
        for i in range(3):
            print("\033[34mUCGT is ready\033[0m")

bot.start()