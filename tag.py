import interactions
from interactions import Modal
import discord
from buttons import buttons

class tag(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  @interactions.extension_command(
    name="tag",
    description="requests a tag for your name; example: [ALOT] Anon",
    scope=582644566641999874)
  async def tag(self, ctx: interactions.CommandContext):
    f = open("tagblacklist.txt", "r")
    new = str(f.read()).rsplit("\n")
    if str(ctx.author.id) in new:
      await ctx.send(f":x: You are blacklisted from requesting tags", ephemeral=True)
      f.close()
      return
    if str(ctx.author.id) not in new:
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

  @interactions.extension_command(
    name="tagblacklist",
    description="blacklists someone from requesting a tag",
    scope=582644566641999874,
    default_member_permissions=interactions.Permissions.BAN_MEMBERS,
    options=[
      interactions.Option(
        name="add",
        description="member to add to the blacklist",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="member",
            description="member to add to the blacklist",
            type=interactions.OptionType.USER,
            required=True)]),
      interactions.Option(
        name="remove",
        description="member to remove from the blacklist",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="member",
            description="member to remove from the blacklist",
            type=interactions.OptionType.USER,
            required=True)]),
      interactions.Option(
        name="list",
        description="shows a list of blacklisted people",
        type=interactions.OptionType.SUB_COMMAND)])
  async def tagblacklist(self, ctx: interactions.CommandContext, sub_command, member: str = None):
    f = open("tagblacklist.txt", "r")
    new = str(f.read()).rsplit("\n")
    if sub_command == "add":
      if str(member.id) in new:
        await ctx.send(f":x: Error! {member.mention} is already blacklisted!", ephemeral=True)
        f.close()
        return
      if str(member.id) not in new:
        b = open("tagblacklist.txt", "a")
        b.writelines([str(member.id), "\n"])
        await ctx.send(f":white_check_mark: Done! Added {member.mention} to the blacklist!", ephemeral=True)
    if sub_command == "remove":
      if str(member.id) not in new:
        await ctx.send(f":x: Error! {member.mention} is not blacklisted!", ephemeral=True)
        return
      if str(member.id) in new:
        with open("tagblacklist.txt", "r") as f:
          lines = f.readlines()
        with open("tagblacklist.txt", "w") as f:
          for line in lines:
            if line.strip("\n") != str(member.id):
              f.write(line)
        await ctx.send(f":white_check_mark: Done! Removed {member.mention} from the blacklist!", ephemeral=True)
    if sub_command == "list":
      new.pop()
      array = []
      for user in new:
        array.append(f"<@!{user}>")
      fuck = "\n".join(array)
      await ctx.send(f"List of people blacklisted from requesting a tag:\n\n{fuck}", ephemeral=True)

  @interactions.extension_listener()
  async def on_ready(penis):
    print("tag has been loaded") 

def setup(bot):
  tag(bot)