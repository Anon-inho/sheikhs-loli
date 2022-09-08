import interactions

bot = interactions.Client(
    token="MTAwMDk2NTYxOTUzMDg2Njc2MA.G1HVv8.V4T_NzW_1HcHO8C3KPl5eX2bI9euRxO1cYbR0w",
    intents=interactions.Intents.ALL)

bot.load("scheduling")
bot.load("confirm")
bot.load("buttons")
bot.load("tickets")
bot.load("inrole")
bot.load("result")

@bot.event
async def on_ready():
        for i in range(3):
            print("\033[34mUCGT is ready\033[0m")

bot.start()