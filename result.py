import interactions
from interactions import SelectMenu, SelectOption
import discord
import buttons
from buttons import buttons

class result(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  option = [interactions.Option(
              name="winners",
              description="Winners team",
              type=interactions.OptionType.ROLE,
              required=True),
              interactions.Option(
                name="losers",
                description="Losers team",
                type=interactions.OptionType.ROLE,
                required=True)]

  @interactions.extension_command(
    name="result", 
    description="Post a match result", 
    scope=582644566641999874,
    options=[
        interactions.Option(
            name="team",
            description="Post the match result for a teams match",
            type=interactions.OptionType.SUB_COMMAND,
            options=option),
        interactions.Option(
            name="trio",
            description="Post the match result for a trios match",
            type=interactions.OptionType.SUB_COMMAND,
            options=option),
        interactions.Option(
            name="duo",
            description="Post the match result for a duos match",
            type=interactions.OptionType.SUB_COMMAND,
            options=option),
        interactions.Option(
            name="other",
            description="Use this for forfeits/scheduling wins",
            type=interactions.OptionType.SUB_COMMAND,
            options=[interactions.Option(
              name="winners",
              description="Winners team",
              type=interactions.OptionType.ROLE,
              required=True),
              interactions.Option(
                name="losers",
                description="Losers team",
                type=interactions.OptionType.ROLE,
                required=True),
              interactions.Option(
                    name="type",
                    description="Whether the match was won by forfeit or scheduling",
                    type=interactions.OptionType.STRING,
                    required=True,
                    choices=[
                        interactions.Choice(
                            name="Forfeit",
                            value="Forfeit"
                        ),
                        interactions.Choice(
                            name="Scheduling",
                            value="Scheduling")])])])
  async def result(self, ctx: interactions.CommandContext, sub_command: str, winners: str = None, losers: str = None, type: str = None):
    if winners.id not in ctx.author.roles and losers.id not in ctx.author.roles:
      await ctx.send(f":x: You must be in one of the participating {sub_command}s to report a match result!", ephemeral=True)
      return
    options1 = []
    options2 = []
    options1.clear()
    options2.clear()
    if sub_command == "team":
      tc = 1045752403951104030
      tcrole = 799846260026769449
      array1 = ["0", "1", "2"]
      simple = "3"
      array2 = ["4", "5", "6"]
      var1 = 3
      var2 = 4
      error = "team"
    if sub_command == "trio":
      tc = 799846360546541589
      tcrole = 702755046387089458
      array1 = ["0", "1"]
      simple = "2"
      array2 = ["3", "4", "5"]
      var1 = 2
      var2 = 3
      error = "trio"
    if sub_command == "duo":
      tc = 703375168801734786
      tcrole = 695116170973675540
      array1 = "0"
      simple = "1"
      array2 = "2"
      var1 = 1
      var2 = 2
      error = "duo"
    elif sub_command == "other":
      teamroles = discord.utils.find(lambda r: r.id == 1045752403951104030, ctx.guild.roles)
      otheroles = discord.utils.find(lambda r: r.id == 695116170973675540, ctx.guild.roles)
      if str(winners.id) in str([799846260026769449, 799846360546541589, 702755046387089458, 703375168801734786]):
        await ctx.send(":x: You may only this with team/trio/duo roles!", ephemeral=True)
        return
      if str(losers.id) in str([799846260026769449, 799846360546541589, 702755046387089458, 703375168801734786]):
        await ctx.send(":x: You may only this with team/trio/duo roles!", ephemeral=True)
        return
      if not teamroles.position > winners.position > otheroles.position:
        await ctx.send(":x: You may only this with team/trio/duo roles!", ephemeral=True)
        return
      if not teamroles.position > losers.position > otheroles.position:
        await ctx.send(":x: You may only this with team/trio/duo roles!", ephemeral=True)
        return
      if ("1045752403951104030" in str(ctx.author.roles)) or ("799846360546541589" in str(ctx.author.roles)) or ("1045752403951104030" in str(ctx.author.roles)):
        if str(winners.id) not in ["799846260026769449", "799846360546541589", "702755046387089458", "703375168801734786"]:
          if str(losers.id) not in ["799846260026769449", "799846360546541589", "702755046387089458", "703375168801734786"]:
            if teamroles.position > winners.position > otheroles.position:
              if teamroles.position > losers.position > otheroles.position:
                resultschannel = discord.utils.find(lambda r: r.id == 881696478052089896, ctx.guild.channels)
                await resultschannel.send(f"**{winners.mention} ({winners.name}): Winners**\n**{losers.mention} ({losers.name}): Losers**\n\n*{type} win*", allowed_mentions={"parse": []})
                return
      if not ("1045752403951104030" in str(ctx.author.roles)) or ("799846360546541589" in str(ctx.author.roles)) or ("1045752403951104030" in str(ctx.author.roles)):
        await ctx.send(":x: You are not a team/trio/duo captain!", ephemeral=True)
        return
    TeamCaptain = discord.utils.find(lambda r: r.id == int(tc), ctx.guild.roles)
    teamrolesrole = discord.utils.find(lambda r: r.id == int(tcrole), ctx.guild.roles)
    if TeamCaptain.id not in ctx.author.roles:
      await ctx.send(f":x: You are not a {TeamCaptain.mention}", ephemeral=True)
      return
    if not TeamCaptain.position > winners.position > teamrolesrole.position:
      await ctx.send(f":x: You can only run this command with {error} roles!", ephemeral=True)
      return
    if not TeamCaptain.position > losers.position > teamrolesrole.position:
      await ctx.send(f":x: You can only run this command with {error} roles!", ephemeral=True)
      return
    if winners.id == losers.id:
      await ctx.send(":x: You must do this with two different roles!", ephemeral=True)
      return
    if TeamCaptain.id in ctx.author.roles:
      if TeamCaptain.position > winners.position > teamrolesrole.position:
          if TeamCaptain.position > losers.position > teamrolesrole.position:
              if winners.id != losers.id:
                await ctx.get_channel()
                await ctx.get_guild()
                await ctx.guild.get_all_members()
                for member in list(ctx.guild.members):
                  if str(winners.id) in str(member.roles):
                    opt1 = SelectOption(label=str(member.name), value=str(f"{member.mention} ({member.name})"))
                    options1.append(opt1)
                  if str(losers.id) in str(member.roles):
                    opt2 = SelectOption(label=str(member.name), value=str(f"{member.mention} ({member.name})"))
                    options2.append(opt2)
                  len1 = len(options1)
                  len2 = len(options2)
                if str(len1) in array1:
                  await ctx.send(f"{winners.mention} does not have enough players to have played a match!", ephemeral=True)
                  return
                if str(len1) in simple:
                  min1 = var1
                  max1 = var1
                if str(len1) in array2:
                  min1 = var1
                  max1 = var2
                if str(len2) in array1:
                  await ctx.send(f"{losers.mention} does not have enough players to have played a match!", ephemeral=True)
                  return
                if str(len2) in simple:
                  min2 = var1
                  max2 = var1
                if str(len2) in array2:
                  min2 = var1
                  max2 = var2
    menu1 = SelectMenu(custom_id="menu1", placeholder=str(winners.name), options=options1, min_values=min1, max_values=max1)
    menu2 = SelectMenu(custom_id="menu2", placeholder=str(losers.name), options=options2, min_values=min2, max_values=max2)
    message1 = await ctx.send(components=menu1, allowed_mentions={"parse": []})
    options1.clear()
    options2.clear()
    global menu2global
    global message1global
    global winnersglobal
    global losersglobal
    global authorglobal
    menu2global = menu2
    message1global = message1
    winnersglobal = winners
    losersglobal = losers
    authorglobal = ctx.author

  menu1array = []
  @interactions.extension_component("menu1")
  async def menu1_response(self, ctx: interactions.ComponentContext, values):
    if str(authorglobal.id) not in str(ctx.author.id):
        ctx.send(":x: Error", ephemeral=True)
    if str(authorglobal.id) in str(ctx.author.id):
        channel = await ctx.get_channel()
        message2 = await channel.send(components=menu2global, allowed_mentions={"parse": []})
        await message1global.delete()
        data = '\n'.join(''.join(o) for o in ctx.data.values)
        result.menu1array.append(data)
        global message2global
        message2global = message2

  menu2array = []
  @interactions.extension_component("menu2")
  async def menu2_response(self, ctx: interactions.ComponentContext, values):
    if str(authorglobal.id) not in str(ctx.author.id):
        ctx.send(":x: Error", ephemeral=True)
    if str(authorglobal.id) in str(ctx.author.id):
        data = '\n'.join(''.join(o) for o in ctx.data.values)
        result.menu2array.append(data)
        await message2global.delete()
        result1 = ''.join(''.join(o) for o in result.menu1array)
        result2 = ''.join(''.join(p) for p in result.menu2array)
        embed = interactions.Embed(
          title="Match Result",
          description=f"**{winnersglobal.name}**\n{str(result1)}\n\n**{losersglobal.name}**\n{str(result2)}\n\n**Winners: {winnersglobal.name}**\n**Losers: {losersglobal.name}**",
          color=int(hex(int("586ce4".replace("#", ""), 16)), 0))
        embed.set_footer(text="United Corporation Governance Tournaments", icon_url="https://cdn.discordapp.com/icons/582644566641999874/565572bdb6c2c4cc6311f44623ef65a1.png")
        await ctx.send(f"**Please check if the match result is correct:**\n:bulb: Tip: if this isn't correct, click the `Cancel` button and try again! Otherwise, click `Confirm`", embeds=embed, components=[buttons.resultconfirm, buttons.resultcancel], ephemeral=True)

  @interactions.extension_component(buttons.resultconfirm.custom_id)
  async def resultconfirm_response(self, ctx: interactions.CommandContext):
    resultschannel = discord.utils.find(lambda r: r.id == 881696478052089896, ctx.guild.channels)
    await ctx.edit(components=[])
    result1 = ''.join(''.join(o) for o in result.menu1array)
    result2 = ''.join(''.join(p) for p in result.menu2array)
    embed = interactions.Embed(
      title="Match Result",
      description=f"**{winnersglobal.name}**\n{str(result1)}\n\n**{losersglobal.name}**\n{str(result2)}\n\n**Winners: {winnersglobal.name}**\n**Losers: {losersglobal.name}**",
      color=int(hex(int("586ce4".replace("#", ""), 16)), 0))
    embed.set_footer(text="United Corporation Governance Tournaments", icon_url="https://cdn.discordapp.com/icons/582644566641999874/565572bdb6c2c4cc6311f44623ef65a1.png")
    await resultschannel.send(embeds=embed)
    result.menu1array.clear()
    result.menu2array.clear()
  
  @interactions.extension_component(buttons.resultcancel.custom_id)
  async def resultcancel_response(self, ctx: interactions.CommandContext):
    await ctx.edit(components=[])
    await ctx.send("Match result cancelled!", ephemeral=True, allowed_mentions={"parse": []})
    result.menu1array.clear()
    result.menu2array.clear()

  @interactions.extension_listener()
  async def on_ready(penis):
    print("result has been loaded") 

def setup(bot):
  result(bot)