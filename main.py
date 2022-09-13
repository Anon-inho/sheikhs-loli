import interactions

bot = interactions.Client(
    token="MTAwMDk2NTYxOTUzMDg2Njc2MA.Gcu5_g.vXh6DNg0lGxheJsMSsI6VoKgcBt89IMgbw9Gjw",
    intents=interactions.Intents.ALL)

bot.load("scheduling")
bot.load("confirm")
bot.load("buttons")
bot.load("tickets")
bot.load("inrole")
bot.load("result")
bot.load("embed")
bot.load("create")

@bot.event
async def on_ready():
        for i in range(3):
            print("\033[34mUCGT is ready\033[0m")

bot.start()