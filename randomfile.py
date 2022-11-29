import interactions
import random
from interactions import Modal
import discord
from buttons import buttons

class randomfile(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  @interactions.extension_command(
    name="whoamibanningtoday",
    description="chooses someone to get banned (fr)",
    scope=582644566641999874,
    default_member_permissions=interactions.Permissions.BAN_MEMBERS,
    options=[
      interactions.Option(
        name="fake",
        description="fake ban",
        type=interactions.OptionType.USER,
        required=False)])
  async def whoamibanningtoday(self, ctx: interactions.CommandContext, fake: str = None):
    if fake == None:
      array = []
      for member in list(ctx.guild.members):
        array.append(member.mention)
      await ctx.send(f"{random.choice(array)} is getting banned today")
    elif fake != None:
      await ctx.send(f"{fake.mention} is getting banned today")

  @interactions.extension_command(
    name="tag",
    description="requests a tag for your name; example: [ALOT] Anon",
    scope=582644566641999874)
  async def tag(self, ctx: interactions.CommandContext):
    modal = Modal(
      title="Tag request",
      custom_id="tag",
      components=[
        interactions.TextInput(style=interactions.TextStyleType.SHORT, custom_id="1", label=f"Tag", required=True, placeholder="Ex: [ALOT]")])
    await ctx.popup(modal)

  @interactions.extension_modal("tag")
  async def tag_response(self, ctx: interactions.CommandContext, one):
    if "[" and "]" in one:
      thing = str(one).upper()
    else:
      thing = f"[{one}]".upper()
    requestchannel = discord.utils.find(lambda r: r.id == 1046461185261830295, ctx.guild.channels)
    await requestchannel.send(f"**Tag request**\n\n**Name:** {ctx.author.mention}\n**Tag:** {thing}", components=[buttons.requesttagapprove, buttons.requesttagdeny])
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

  @interactions.extension_component(buttons.requesttagdeny.custom_id)
  async def tagdeny_response(self, ctx: interactions.CommandContext):
    array = str(ctx.message.content).replace("**", "").replace("Tag request", "").replace("Name: ", "").replace("Tag: ", "").replace("\n\n", "").rsplit("\n")
    lobby = discord.utils.find(lambda r: r.id == 582646950403506199, ctx.guild.channels)
    await lobby.send(f":x: {array[0]}, your **tag request** was **denied**")
    await ctx.edit(content=f"{ctx.message.content}\n\n:x: **Denied by {ctx.author.mention}**", components=[])

  @interactions.extension_listener()
  async def on_ready(penis):
    print("random has been loaded") 

def setup(bot):
  randomfile(bot)