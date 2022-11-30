import interactions
from interactions import Modal
import discord
from buttons import buttons

class request(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  @interactions.extension_command(
    name="request",
    description="Requests the creation of a corporation",
    scope=582644566641999874,
    options=[
      interactions.Option(
        name="create",
        description="creates",
        type=interactions.OptionType.SUB_COMMAND_GROUP,
        options=[
          interactions.Option(
            name="team",
            description="Requests the creation of a team",
            type=interactions.OptionType.SUB_COMMAND),
          interactions.Option(
            name="trio",
            description="Requests the creation of a trio",
            type=interactions.OptionType.SUB_COMMAND),
          interactions.Option(
            name="duo",
            description="Requests the creation of a duo",
            type=interactions.OptionType.SUB_COMMAND)]),
        interactions.Option(
          name="join",
          description="Requests to join a corporation",
          type=interactions.OptionType.SUB_COMMAND_GROUP,
          options=[
            interactions.Option(
            name="team",
            description="Requests to join a team",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
              interactions.Option(
                name="name",
                description="Name of the team you want to join",
                type=interactions.OptionType.ROLE,
                required=True)]),
          interactions.Option(
            name="trio",
            description="Requests to join a trio",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
              interactions.Option(
                name="name",
                description="Name of the trio you want to join",
                type=interactions.OptionType.ROLE,
                required=True)]),
          interactions.Option(
            name="duo",
            description="Requests to join a duo",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
              interactions.Option(
                name="name",
                description="Name of the trio you want to join",
                type=interactions.OptionType.ROLE,
                required=True)])])])
  async def request(self, ctx: interactions.CommandContext, sub_command_group, sub_command, name: str = None):
    if sub_command_group == "create":
      if sub_command == "team":
        tc = 594347203171057668
        tcrole = 799846260026769449
      if sub_command == "trio":
        tc = 799846260026769449
        tcrole = 702755046387089458
      if sub_command == "duo":
        tc = 702755046387089458
        tcrole = 695116170973675540
      await ctx.guild.get_all_roles()
      teamcaptainrole = discord.utils.find(lambda r: r.id == int(tc), ctx.guild.roles)
      teamrolesrole = discord.utils.find(lambda r: r.id == int(tcrole), ctx.guild.roles)
      thing = []
      for role in ctx.author.roles:
        new = discord.utils.find(lambda r: r.id == int(role), ctx.guild.roles)
        if teamcaptainrole.position > new.position > teamrolesrole.position:
          thing.append(new)
      if thing != []:
        await ctx.send(f":x: You are already in a {sub_command}", ephemeral=True)
        return
      if thing == []:
        createmodal = Modal(
          custom_id="createmodal",
          title=f"Create a {sub_command}",
          components=[
            interactions.TextInput(style=interactions.TextStyleType.SHORT, custom_id="1", label=f"{sub_command} name", required=True),
            interactions.TextInput(style=interactions.TextStyleType.SHORT, custom_id="2", label=f"Role color (in hex)", required=True),
            interactions.TextInput(style=interactions.TextStyleType.SHORT, custom_id="3", label=f"{sub_command} members")])
        await ctx.popup(createmodal)
    if sub_command_group == "join":
      if sub_command == "team":
        tc = 594347203171057668
        tcrole = 799846260026769449
      if sub_command == "trio":
        tc = 799846260026769449
        tcrole = 702755046387089458
      if sub_command == "duo":
        tc = 702755046387089458
        tcrole = 695116170973675540
      await ctx.guild.get_all_roles()
      teamcaptainrole = discord.utils.find(lambda r: r.id == int(tc), ctx.guild.roles)
      teamrolesrole = discord.utils.find(lambda r: r.id == int(tcrole), ctx.guild.roles)
      if not teamcaptainrole.position-1 > name.position > teamrolesrole.position:
        await ctx.send(f":x: That's not a {sub_command}", ephemeral=True)
        return
      thing = []
      for role in ctx.author.roles:
        new = discord.utils.find(lambda r: r.id == int(role), ctx.guild.roles)
        if teamcaptainrole.position > new.position > teamrolesrole.position:
          thing.append(new)
      if thing != []:
        await ctx.send(f":x: You are already in a {sub_command}", ephemeral=True)
        return
      if thing == []:
        requestchannel = discord.utils.find(lambda r: r.id == 1046461185261830295, ctx.guild.channels)
        await requestchannel.send(f"**{str(sub_command).capitalize()} join request:**\n\n**Name:** {ctx.author.mention}\n**{str(sub_command).capitalize()}:** {name.mention}", components=[buttons.requestjoinapprove, buttons.requestjoindeny])
        await ctx.send(":white_check_mark: Done! Request sent to <@&582646886696091669>", ephemeral=True)
    global globalsubcommand
    globalsubcommand = sub_command
    thing.clear()

  @interactions.extension_modal("createmodal")
  async def createmodal_response(self, ctx: interactions.CommandContext, one, two, three):
    requestchannel = discord.utils.find(lambda r: r.id == 1046461185261830295, ctx.guild.channels)
    await requestchannel.send(f"**{str(globalsubcommand).capitalize()} creation request:**\n\n**Name:** {one}\n**Color:** {two}\n**Captain:** {ctx.author.mention}\n**{str(globalsubcommand).capitalize()} members:** {three}", components=[buttons.requestcreateapprove, buttons.requestcreatedeny])
    await ctx.send(":white_check_mark: Request sent to <@&582646886696091669>", ephemeral=True)

  @interactions.extension_component(buttons.requestcreateapprove.custom_id)
  async def requestcreateapprove_response(self, ctx: interactions.CommandContext):
    if ctx.message.content.startswith("**Team") == True:
      tc = discord.utils.find(lambda r: r.id == 1045752403951104030, ctx.guild.roles)
      position = tc.position
      var = "team"
    if ctx.message.content.startswith("**Trio") == True:
      tc = discord.utils.find(lambda r: r.id == 799846360546541589, ctx.guild.roles)
      position = tc.position
      var = "trio"
    if ctx.message.content.startswith("**Duo") == True:
      tc = discord.utils.find(lambda r: r.id == 703375168801734786, ctx.guild.roles)
      position = tc.position
      var = "duo"
    array = str(ctx.message.content).replace("**Team creation request:**", "").replace("**Trio creation request:**", "").replace("**Duo creation request:**", "").replace("**Name:** ", "").replace("**Color:** ", "").replace("**Captain:** ", "").replace("**Team members:** ", "").replace("**Trio members:** ", "").replace("**Duo members:** ", "").replace("\n\n", "").rsplit("\n")
    role = await ctx.guild.create_role(
      name=array[0],
      color=int(hex(int(array[1].replace("#", ""), 16)), 0))
    await ctx.guild.modify_role_position(role_id=int(role.id), position=position)
    await ctx.guild.add_member_role(role=role.id, member_id=int(array[2].replace("<@!", "").replace(">", "")))
    await ctx.guild.add_member_role(role=tc.id, member_id=int(array[2].replace("<@!", "").replace(">", "")))
    lobby = discord.utils.find(lambda r: r.id == 582646950403506199, ctx.guild.channels)
    await lobby.send(f":white_check_mark: {array[2]}, your **{var} creation** request was **approved**")
    await ctx.edit(content=f"{ctx.message.content}\n\n:white_check_mark: **Approved by {ctx.author.mention}**", components=[], allowed_mentions={"parse": ["users"]})

  @interactions.extension_component(buttons.requestcreatedeny.custom_id)
  async def requestcreatedeny_response(self, ctx: interactions.CommandContext):
    createdenymodal = Modal(
      custom_id="createdenymodal",
      title="Deny reason",
      components=[interactions.TextInput(style=interactions.TextStyleType.PARAGRAPH, label="Deny reason", max_length=500, custom_id="1", placeholder="Example: You suck")])
    await ctx.popup(createdenymodal)
    global globalmsg
    globalmsg = ctx.message

  @interactions.extension_modal("createdenymodal")
  async def createdenymodal_response(self, ctx: interactions.CommandContext, one):
    if ctx.message.content.startswith("**Team") == True:
      var = "team"
    if ctx.message.content.startswith("**Trio") == True:
      var = "trio"
    if ctx.message.content.startswith("**Duo") == True:
      var = "duo"
    array = str(ctx.message.content).replace("**Team creation request:**", "").replace("**Trio creation request:**", "").replace("**Duo creation request:**", "").replace("**Name:** ", "").replace("**Color:** ", "").replace("**Captain:** ", "").replace("**Team members:** ", "").replace("**Trio members:** ", "").replace("**Duo members:** ", "").replace("\n\n", "").rsplit("\n")
    lobby = discord.utils.find(lambda r: r.id == 582646950403506199, ctx.guild.channels)
    await lobby.send(f":x: {array[2]}, your **{var} creation** request was **denied**\n\n**Reason:** {one}", allowed_mentions={"parse": ["users"]})
    await globalmsg.edit(content=f"{ctx.message.content}\n\n**:x: Denied by {ctx.author.mention}**", components=[])

  @interactions.extension_component(buttons.requestjoinapprove.custom_id)
  async def requestjoinapprove_response(self, ctx: interactions.CommandContext):
    array1 = str(ctx.message.content).replace("**Team join request:", "").replace("**Trio join request:", "").replace("**Duo join request:", "").replace("**Name:** ", "").replace("**Team:** ", "").replace("**Trio:** ", "").replace("**Duo:** ", "").replace("\n\n", "").rsplit("\n")
    await ctx.guild.add_member_role(role=int(array1[1].replace("<@&", "").replace(">", "")), member_id=int(array1[0].replace("**<@!", "").replace(">", "").replace("**<@", "")))
    lobby = discord.utils.find(lambda r: r.id == 582646950403506199, ctx.guild.channels)
    retard = array1[0].replace("**", "")
    await lobby.send(f":white_check_mark: {retard}, your **request to join** {array1[1]} was **approved**", allowed_mentions={"parse": ["users"]})
    await ctx.edit(content=f"{ctx.message.content}\n\n:white_check_mark: **Approved by {ctx.author.mention}**", components=[])

  @interactions.extension_component(buttons.requestjoindeny.custom_id)
  async def requestjoindeny_response(self, ctx: interactions.CommandContext):
    array = str(ctx.message.content).replace("**Team join request:**", "").replace("**Trio join request:**", "").replace("**Duo join request:**", "").replace("**Name:** ", "").replace("**Team:** ", "").replace("**Trio:** ", "").replace("**Duo:** ", "").replace("\n\n", "").rsplit("\n")
    lobby = discord.utils.find(lambda r: r.id == 582646950403506199, ctx.guild.channels)
    await lobby.send(f":x: {array[0]}, your **request to join** {array[1]} was **denied**", allowed_mentions={"parse": ["users"]})
    await ctx.edit(content=f"{ctx.message.content}\n\n:x: **Denied by {ctx.author.mention}**", components=[])

  @interactions.extension_listener()
  async def on_ready(penis):
    print("request has been loaded") 

def setup(bot):
  request(bot)