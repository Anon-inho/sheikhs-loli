import interactions
from interactions import Modal
import discord

class create(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  modal = Modal(
      custom_id="create",
      title="Corporation building",
      components=[
        interactions.TextInput(custom_id="1", style=interactions.TextStyleType.SHORT, label="Team Name", placeholder="fog bad", required=True),
        interactions.TextInput(custom_id="2", style=interactions.TextStyleType.SHORT, label="Role Color", placeholder="123456", required=True)])

  option=[
    interactions.Option(
      name="captain",
      description="corporation captain",
      type=interactions.OptionType.USER,
      required=False)]

  @interactions.extension_command(
    name="create",
    description="Creates a corporation (role)",
    scope=582644566641999874,
    default_member_permissions=interactions.Permissions.MANAGE_ROLES,
    options=[
      interactions.Option(
        name="team",
        description="Creates a team",
        type=interactions.OptionType.SUB_COMMAND,
        options=option),
      interactions.Option(
        name="trio",
        description="Creates a trio",
        type=interactions.OptionType.SUB_COMMAND,
        options=option),
      interactions.Option(
        name="duo",
        description="Creates a duo",
        type=interactions.OptionType.SUB_COMMAND,
        options=option)])
  async def create(self, ctx: interactions.CommandContext, sub_command: str, captain: str = None):
    if sub_command == "team":
      position=1045752403951104030
    if sub_command == "trio":
      position=799846360546541589
    if sub_command == "duo":
      position=703375168801734786
    await ctx.popup(create.modal)
    global globalposition
    global globalcaptain
    globalposition = position
    globalcaptain = captain

  @interactions.extension_modal("create")
  async def create_response(self, ctx: interactions.CommandContext, one, two):
    roleposition = discord.utils.find(lambda r: r.id == int(globalposition), ctx.guild.roles)
    readableHex = int(hex(int(str(two).replace("#", ""), 16)), 0)
    role = await ctx.guild.create_role(name=one, color=readableHex)
    await ctx.guild.modify_role_position(role_id=int(role.id), position=roleposition.position)
    if globalcaptain != None:
      await ctx.guild.add_member_role(role=roleposition, member_id=globalcaptain.id)
      await ctx.guild.add_member_role(role=role, member_id=globalcaptain.id)
    await ctx.send(f":white_check_mark: Done! Created {role.mention}")

  @interactions.extension_listener()
  async def on_ready(penis):
    print("create has been loaded") 

def setup(bot):
  create(bot)