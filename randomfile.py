import interactions
import random

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

  @interactions.extension_listener()
  async def on_ready(penis):
    print("random has been loaded") 

def setup(bot):
  randomfile(bot)