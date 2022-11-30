import interactions
from interactions import Modal
import discord
from buttons import buttons
import os

class tag(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  @interactions.extension_command(
    name="tag",
    description="requests a tag for your name; example: [ALOT] Anon",
    scope=582644566641999874)
  async def tag(self, ctx: interactions.CommandContext):
    f = open(os.getcwd() + "\\..\\blacklists\\tagblacklist.txt", "r")
    new = str(f.read()).rsplit("\n")
    if str(ctx.author.id) in new:
      await ctx.send(f":x: You are blacklisted from requesting tags", ephemeral=True)
      f.close()
      return
    if str(ctx.author.id) not in new:
      thing = int(29-ctx.author.name.__len__())
      if thing <= 2:
        await ctx.send(":x: Your nickname is too long to request a tag, please ask for one manually", ephemeral=True)
        return
      if thing > 2:
        modal = Modal(
          title="Tag request",
          custom_id="tag",
          components=[
            interactions.TextInput(style=interactions.TextStyleType.SHORT, custom_id="1", label=f"Tag", required=True, placeholder="Ex: [ALOT]", max_length=thing)])
        await ctx.popup(modal)

  @interactions.extension_modal("tag")
  async def tag_response(self, ctx: interactions.CommandContext, one):
    if "[" and "]" in one:
      thing = str(one).upper()
    else:
      thing = f"[{one}]".upper()
    if "[" and "]" in ctx.author.name:
      button = [buttons.requesttagapprove, buttons.requesttagreplace, buttons.requesttagdeny]
    else:
      button = [buttons.requesttagapprove, buttons.requesttagdeny]
    requestchannel = discord.utils.find(lambda r: r.id == 1046461185261830295, ctx.guild.channels)
    await requestchannel.send(f"**Tag request**\n\n**Name:** {ctx.author.mention}\n**Tag:** {thing}", components=button)
    await ctx.send(":white_check_mark: Done! Tag request sent to <@&582646886696091669>", ephemeral=True)

  @interactions.extension_component(buttons.requesttagapprove.custom_id)
  async def tagapprove_response(self, ctx: interactions.CommandContext):
    array = str(ctx.message.content).replace("**", "").replace("Tag request", "").replace("Name: ", "").replace("Tag: ", "").replace("\n\n", "").rsplit("\n")
    user = discord.utils.find(lambda r: r.id == int(array[0].replace("<@!", "").replace(">", "").replace("<@", "")), ctx.guild.members)
    await ctx.guild.modify_member(
      member_id=int(array[0].replace("<@!", "").replace(">", "").replace("<@", "")), 
      nick=f"{array[1]} {user.name}")
    lobby = discord.utils.find(lambda r: r.id == 582646950403506199, ctx.guild.channels)
    await lobby.send(f":white_check_mark: {array[0]}, your **tag request** was **approved**")
    await ctx.edit(content=f"{ctx.message.content}\n\n:white_check_mark: **Approved by {ctx.author.mention}**", components=[])

  @interactions.extension_component(buttons.requesttagreplace.custom_id)
  async def tagreplace_response(self, ctx: interactions.CommandContext):
    array = str(ctx.message.content).replace("**", "").replace("Tag request", "").replace("Name: ", "").replace("Tag: ", "").replace("\n\n", "").rsplit("\n")
    lobby = discord.utils.find(lambda r: r.id == 582646950403506199, ctx.guild.channels)
    user = discord.utils.find(lambda r: r.id == int(array[0].replace("<@!", "").replace(">", "").replace("<@", "")), ctx.guild.members)
    tuple = list(str(user.name).partition("]"))
    name = tuple[2].replace(" ", "", 1)
    await ctx.guild.modify_member(
      member_id=int(array[0].replace("<@!", "").replace(">", "").replace("<@", "")), 
      nick=f"{array[1]} {name}")
    await lobby.send(f":white_check_mark: {array[0]}, your **tag request** was **approved**")
    await ctx.edit(content=f"{ctx.message.content}\n\n:white_check_mark: **Approved by {ctx.author.mention}**", components=[])

  @interactions.extension_component(buttons.requesttagdeny.custom_id)
  async def tagdeny_response(self, ctx: interactions.CommandContext):
    array = str(ctx.message.content).replace("**", "").replace("Tag request", "").replace("Name: ", "").replace("Tag: ", "").replace("\n\n", "").rsplit("\n")
    lobby = discord.utils.find(lambda r: r.id == 582646950403506199, ctx.guild.channels)
    await lobby.send(f":x: {array[0]}, your **tag request** was **denied**")
    await ctx.edit(content=f"{ctx.message.content}\n\n:x: **Denied by {ctx.author.mention}**", components=[])

  @interactions.extension_listener()
  async def on_ready(penis):
    print("tag has been loaded") 

def setup(bot):
  tag(bot)