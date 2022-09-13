import interactions
import discord

class scheduling(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  option = [
              interactions.Option(
                name="role1",
                description="role1",
                type=interactions.OptionType.ROLE,
                required=True),
              interactions.Option(
                name="role2",
                description="role2",
                type=interactions.OptionType.ROLE,
                required=True),
              interactions.Option(
                name="ephemeral",
                description="whether the message will appear only for you; useful for using this command in #brackets",
                type=interactions.OptionType.STRING,
                required=False,
                choices=[
                  interactions.Choice(
                    name="true",
                    value="True"),
                  interactions.Choice(
                    name="false",
                    value="False")])]

  @interactions.extension_command(
    name="scheduling",
    description="Creates a scheduling channel",
    default_member_permissions=interactions.Permissions.MANAGE_CHANNELS,
    scope=582644566641999874,
    options=[
        interactions.Option(
            name="team",
            description="Creates a scheduling channel for teams",
            type=interactions.OptionType.SUB_COMMAND,
            options=option),
        interactions.Option(
            name="trio",
            description="Creates a scheduling channel for trios",
            type=interactions.OptionType.SUB_COMMAND,
            options=option),
        interactions.Option(
            name="duo",
            description="Creates a scheduling channel for duos",
            type=interactions.OptionType.SUB_COMMAND,
            options=option)])
  async def scheduling(self, ctx: interactions.CommandContext, sub_command: str, role1, role2, ephemeral: str = ""):
    await ctx.get_guild()
    if sub_command == "team":
      category = 1001966433372213409
      TeamCaptain = discord.utils.find(lambda r: r.id == 694367677262725212, ctx.guild.roles)
      teamrolesrole = discord.utils.find(lambda r: r.id == int(799846260026769449), ctx.guild.roles)
      teams = "4v4, 4v3 or 3v3"
    if sub_command == "trio":
      category = 1002353768320466955
      TeamCaptain = discord.utils.find(lambda r: r.id == 799846360546541589, ctx.guild.roles)
      teamrolesrole = discord.utils.find(lambda r: r.id == int(702755046387089458), ctx.guild.roles)
      teams = "3v3, 3v2 or 2v2"
    if sub_command == "duo":
      category = 1001966453089632399
      TeamCaptain = discord.utils.find(lambda r: r.id == 703375168801734786, ctx.guild.roles)
      teamrolesrole = discord.utils.find(lambda r: r.id == int(695116170973675540), ctx.guild.roles)
      teams = "2v2, 2v1 or 1v1"
    if ephemeral == "False":
      ephemeral = False
    if not TeamCaptain.position > role1.position > teamrolesrole.position:
      await ctx.send(f":x: You can only run this command with {sub_command} roles!", ephemeral=True)
      return
    if not TeamCaptain.position > role2.position > teamrolesrole.position:
      await ctx.send(f":x: You can only run this command with {sub_command} roles!", ephemeral=True)
      return
    if role1.id == role2.id:
      await ctx.send(":x: You must do this with two different roles!", ephemeral=True)
      return
    channel = await ctx.guild.create_channel(
            name=f"{role1.name} vs {role2.name}", 
            type=interactions.ChannelType.GUILD_TEXT, 
            parent_id=category,
            permission_overwrites=[interactions.Overwrite(id=str(role1.id), type=0, allow=interactions.Permissions.VIEW_CHANNEL | interactions.Permissions.SEND_MESSAGES | interactions.Permissions.EMBED_LINKS | interactions.Permissions.ATTACH_FILES),
            interactions.Overwrite(id=str(role2.id), type=0, allow=interactions.Permissions.VIEW_CHANNEL | interactions.Permissions.SEND_MESSAGES | interactions.Permissions.EMBED_LINKS | interactions.Permissions.ATTACH_FILES),
            interactions.Overwrite(id=str(582646886696091669), type=0, allow=interactions.Permissions.VIEW_CHANNEL | interactions.Permissions.SEND_MESSAGES | interactions.Permissions.EMBED_LINKS | interactions.Permissions.ATTACH_FILES | interactions.Permissions.MANAGE_CHANNELS | interactions.Permissions.MANAGE_ROLES | interactions.Permissions.MENTION_EVERYONE),
            interactions.Overwrite(id=str(582644566641999874), type=0, deny=interactions.Permissions.VIEW_CHANNEL)])
    message = await channel.send(f"Hello!\n\nOne {sub_command} captain, from either {sub_command}, must run `/confirm {sub_command}`; after filling out the details, the other team captain must click the confirm button; once these two steps are done, a Staff member will officially confirm the match.\nNote: The team size must be {teams}\n\n*Failure to confirm a match will result in a failure of scheduling for both teams, and if this happens Staff will give the forfeit to the team who has shown less efforts to schedule.*\n\nRead <#589237674129358851> for the deadline and more info\n\n<@&{role1.id}> <@&{role2.id}>", allowed_mentions={"parse": ["users", "roles"]})
    await channel.pin_message(message)
    await ctx.send(f":white_check_mark: Done! Created scheduling channel for **{sub_command}s**: {role1.mention} and {role2.mention}: {channel.mention}", allowed_mentions={"parse": []}, ephemeral=ephemeral)
    
  @interactions.extension_listener()
  async def on_ready(penis):
    print("scheduling has been loaded")

def setup(bot):
  scheduling(bot)