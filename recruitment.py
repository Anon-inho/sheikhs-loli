import interactions
from interactions import Embed, Modal
import discord
import os

class recruitment(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  @interactions.extension_command(
    name="recruitment",
    description="posts a recruitment message",
    scope=582644566641999874,
    options=[
      interactions.Option(
        name="create",
        description="Use this if you are trying to create a team/trio/duo",
        type=interactions.OptionType.SUB_COMMAND),
      interactions.Option(
        name="join",
        description="Use this if you are trying to join a team/trio/duo",
        type=interactions.OptionType.SUB_COMMAND)])
  async def recruitment(self, ctx: interactions.CommandContext, sub_command):
    f = open(os.getcwd() + "\\blacklists\\recruitmentblacklist.txt", "r")
    new = str(f.read()).rsplit("\n")
    if str(ctx.author.id) in new:
      await ctx.send(f":x: You are blacklisted from posting a recruitment", ephemeral=True)
      f.close()
      return
    if str(ctx.author.id) not in new:
      if sub_command == "create":
        modal = Modal(
          title=f"{str(sub_command).capitalize()} a team/trio/duo",
          custom_id="recruitment",
          components=[
            interactions.TextInput(style=interactions.TextStyleType.SHORT, label=f"Creating a [team/trio]duo]", placeholder="Ex: Trio", custom_id="1"),
            interactions.TextInput(style=interactions.TextStyleType.SHORT, label=f"What's the rating needed to join?", placeholder="Ex: 2826", custom_id="2"),
            interactions.TextInput(style=interactions.TextStyleType.SHORT, label=f"What are the strengths needed to join?", placeholder="Ex: Aiming", custom_id="3"),
            interactions.TextInput(style=interactions.TextStyleType.SHORT, label=f"What availability should people have to join?", placeholder="Ex: 2 PM - 10 PM EST", custom_id="4")])
      if sub_command == "join":
        modal = Modal(
          title=f"{str(sub_command).capitalize()} a team/trio/duo",
          custom_id="recruitment",
          components=[
            interactions.TextInput(style=interactions.TextStyleType.SHORT, label=f"Joining a [team/trio/duo]", placeholder="Ex: Trio", custom_id="1"),
            interactions.TextInput(style=interactions.TextStyleType.SHORT, label=f"What's your rating?", placeholder="Ex: 2826", custom_id="2"),
            interactions.TextInput(style=interactions.TextStyleType.SHORT, label=f"What are your strengths?", placeholder="Ex: Aiming", custom_id="3"),
            interactions.TextInput(style=interactions.TextStyleType.SHORT, label=f"What about your weaknesses?", placeholder="Ex: Sky basing", custom_id="4"),
            interactions.TextInput(style=interactions.TextStyleType.SHORT, label=f"What your availiability?", placeholder="Ex: 2 PM - 10 PM EST", custom_id="5")])
      await ctx.popup(modal)
      global globalsubcommand
      globalsubcommand = sub_command

  @interactions.extension_modal("recruitment")
  async def recruitment_response(self, ctx: interactions.CommandContext, one, two, three, four, five: str = None):
    if five == None:
      embed = Embed(
        title=ctx.author.name,
        description=f"**Looking to:** {globalsubcommand} a {one}\n**Rating needed to join:** {two}\n**Strengths needed to join:** {three}\n**Recommended availability:** {four}",
        color=int(hex(int("586ce4".replace("#", ""), 16)), 0))
    if five != None:
      embed = Embed(
        title=ctx.author.name,
        description=f"**Looking to:** {globalsubcommand} a {one}\n**Rating:** {two}\n**Strengths:** {three}\n**Weaknesses:** {four}\n**Availability:** {five}",
        color=int(hex(int("586ce4".replace("#", ""), 16)), 0))
    recruitmentchannel = discord.utils.find(lambda r: r.id == 888161164654170143, ctx.guild.channels)
    await recruitmentchannel.send(content="Type `/recruitment` in any channel to send a message here", embeds=embed)
    await ctx.send(f":white_check_mark: Your message was sent to {recruitmentchannel.mention}", ephemeral=True)

  @interactions.extension_listener()
  async def on_ready(penis):
    print("recruitment has been loaded") 

def setup(bot):
  recruitment(bot)