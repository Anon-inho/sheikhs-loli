import interactions
import os

class blacklist(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  choice = []
  for item in os.listdir(os.getcwd() + "\\..\\blacklists"):
    choice.append(
      interactions.Choice(
        name=item.replace("blacklist.txt", "").capitalize(),
        value=item.replace("blacklist.txt", "")))

  @interactions.extension_command(
    name="blacklist",
    description="various blacklist actions",
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
            required=True),
          interactions.Option(
            name="name",
            description="which blacklist",
            type=interactions.OptionType.STRING,
            required=True,
            choices=choice)]),
      interactions.Option(
        name="remove",
        description="member to remove from the blacklist",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="member",
            description="member to remove from the blacklist",
            type=interactions.OptionType.USER,
            required=True),
          interactions.Option(
            name="name",
            description="which blacklist",
            type=interactions.OptionType.STRING,
            required=True,
            choices=choice)]),
      interactions.Option(
        name="list",
        description="shows a list of blacklisted people",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="name",
            description="which blacklist",
            type=interactions.OptionType.STRING,
            required=True,
            choices=choice)])])
  async def tagblacklist(self, ctx: interactions.CommandContext, sub_command, member: str = None, name: str = None):
    f = open(os.getcwd() + f"\\..\\blacklists\\{name}blacklist.txt", "r")
    new = str(f.read()).rsplit("\n")
    if sub_command == "add":
      if str(member.id) in new:
        await ctx.send(f":x: Error! {member.mention} is already blacklisted from {name}s!", ephemeral=True)
        f.close()
        return
      if str(member.id) not in new:
        b = open(os.getcwd() + f"\\..\\blacklists\\{name}blacklist.txt", "a")
        b.writelines([str(member.id), "\n"])
        await ctx.send(f":white_check_mark: Done! Added {member.mention} to the {name} blacklist!", ephemeral=True)
    if sub_command == "remove":
      if str(member.id) not in new:
        await ctx.send(f":x: Error! {member.mention} is not blacklisted from {name}s!", ephemeral=True)
        return
      if str(member.id) in new:
        with open(os.getcwd() + f"\\..\\blacklists\\{name}blacklist.txt", "r") as f:
          lines = f.readlines()
        with open(os.getcwd() + f"\\..\\blacklists\\{name}blacklist.txt", "w") as f:
          for line in lines:
            if line.strip("\n") != str(member.id):
              f.write(line)
        await ctx.send(f":white_check_mark: Done! Removed {member.mention} from the {name} blacklist!", ephemeral=True)
    if sub_command == "list":
      new.pop()
      array = []
      for user in new:
        array.append(f"<@!{user}>")
      fuck = "\n".join(array)
      await ctx.send(f"List of people blacklisted from {name}s:\n\n{fuck}", ephemeral=True)

  @interactions.extension_listener()
  async def on_ready(penis):
    print("blacklist has been loaded") 

def setup(bot):
  blacklist(bot)