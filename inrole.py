import interactions
import discord

class inrole(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  option = [interactions.Option(
    name="ephemeral",
    description="Whether the message will appear to everyone",
    type=interactions.OptionType.STRING,
    required=False,
    choices=[
      interactions.Choice(
        name="True",
        value="True"),
      interactions.Choice(
      name="False",
      value="False")])]

  option2 = [
    interactions.Option(
        name="role",
        description="Role to inrole",
        type=interactions.OptionType.ROLE,
        required=True),
    interactions.Option(
    name="ephemeral",
    description="Whether the message will appear to everyone",
    type=interactions.OptionType.STRING,
    required=False,
    choices=[
      interactions.Choice(
        name="True",
        value="True"),
      interactions.Choice(
      name="False",
      value="False")])]

  @interactions.extension_command(
    name="inrole", 
    description="See current corporations", 
    scope=582644566641999874,
    options=[
        interactions.Option(
            name="teams",
            description="Shows all current teams",
            type=interactions.OptionType.SUB_COMMAND,
            options=option),
        interactions.Option(
            name="trios",
            description="Shows all current trios",
            type=interactions.OptionType.SUB_COMMAND,
            options=option),
        interactions.Option(
            name="duos",
            description="Shows all current duos",
            type=interactions.OptionType.SUB_COMMAND,
            options=option),
        interactions.Option(
            name="role",
            description="Role to inrole",
            type=interactions.OptionType.SUB_COMMAND,
            options=option2)])
  async def inrole(self, ctx: interactions.CommandContext, sub_command: str, role: str = None, ephemeral: str = None):
    Staff = discord.utils.find(lambda r: r.id == 582646886696091669, ctx.guild.roles)
    if ephemeral == "False":
      ephemeral = False
    if sub_command == "teams":
      tc = 1045752403951104030
      tcrole = 799846260026769449
    if sub_command == "trios":
      tc = 799846360546541589
      tcrole = 702755046387089458
    if sub_command == "duos":
      tc = 703375168801734786
      tcrole = 695116170973675540
    if sub_command == "role":
      if str(role.id) in str([799846260026769449, 702755046387089458]):
        await ctx.send(":x: You may only inrole corporations or corporation captains!", ephemeral=True)
        return
      teamroles = discord.utils.find(lambda r: r.id == 594347203171057668, ctx.guild.roles)
      otheroles = discord.utils.find(lambda r: r.id == 695116170973675540, ctx.guild.roles)
      if Staff.id not in ctx.author.roles:
        if not teamroles.position > role.position > otheroles.position:
          await ctx.send(":x: You may only inrole corporations or corporation captains!", ephemeral=True)
          return
        if str(ctx.channel_id) not in "582646964466745364":
          ephemeral = True
      if str(role.id) not in str(799846260026769449) or str(702755046387089458):
          await ctx.guild.get_all_members()
          names = []
          for member in list(ctx.guild.members):
              if str(role.id) in str(member.roles):
                  names.append(f"{member.mention} ({member.name})")
      await ctx.send(f"Members in {role.mention}:\n\n" + str('\n'.join(names)), allowed_mentions={"parse": []}, ephemeral=ephemeral)
      return
    await ctx.guild.get_all_roles()
    teamcaptainrole = discord.utils.find(lambda r: r.id == int(tc), ctx.guild.roles)
    teamrolesrole = discord.utils.find(lambda r: r.id == int(tcrole), ctx.guild.roles)
    names1 = []
    for role in list(ctx.guild.roles):
      if teamcaptainrole.position > role.position > teamrolesrole.position:
          names1.append(f"{role.mention} ({role.name})")
    await ctx.get_channel()
    if Staff.id not in ctx.author.roles:
      if str(ctx.channel_id) not in "582646964466745364":
        ephemeral = True
    await ctx.send("Current teams:\n\n" + str('\n'.join(names1)), allowed_mentions={"parse": []}, ephemeral=ephemeral)
    names1.clear()

  @interactions.extension_listener()
  async def on_ready(penis):
    print("inrole has been loaded") 

def setup(bot):
  inrole(bot)