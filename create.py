import interactions
from interactions import Modal, Embed
import discord

class create(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  option=[
    interactions.Option(
      name="name",
      description="role name",
      type=interactions.OptionType.STRING,
      required=True),
    interactions.Option(
      name="color",
      description="role color (in hex)",
      type=interactions.OptionType.STRING,
      required=True),
    interactions.Option(
      name="captain",
      description="corporation captain",
      type=interactions.OptionType.USER,
      required=False)]

  @interactions.extension_command(
    name="create",
    description="creates corporations",
    scope=582644566641999874,
    default_member_permissions=interactions.Permissions.MANAGE_ROLES,
    options=[
      interactions.Option(
        name="team",
        description="creates a team",
        type=interactions.OptionType.SUB_COMMAND,
        options=option),
      interactions.Option(
        name="trio",
        description="creates a trio",
        type=interactions.OptionType.SUB_COMMAND,
        options=option),
      interactions.Option(
        name="duo",
        description="creates a duo",
        type=interactions.OptionType.SUB_COMMAND,
        options=option)])
  async def create(self, ctx: interactions.CommandContext, sub_command: str, name, color, captain: str = None):
    if sub_command == "team":
      position=694367677262725212
    if sub_command == "trio":
      position=799846360546541589
    if sub_command == "duo":
      position=703375168801734786
    roleposition = discord.utils.find(lambda r: r.id == int(position), ctx.guild.roles)
    readableHex = int(hex(int(color.replace("#", ""), 16)), 0)
    role = await ctx.guild.create_role(name=name, color=readableHex)
    await ctx.guild.modify_role_position(role_id=int(role.id), position=roleposition.position-1)
    if captain != None:
      await ctx.guild.add_member_role(role=roleposition, member_id=captain.id)
      await ctx.guild.add_member_role(role=role, member_id=captain.id)
    await ctx.send(f":white_check_mark: Done! Created {sub_command}: {role.mention}")

  @interactions.extension_listener()
  async def on_ready(penis):
    print("embed has been loaded") 

def setup(bot):
  create(bot)