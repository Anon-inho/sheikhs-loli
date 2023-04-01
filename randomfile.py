import interactions
import random
from PIL import Image, ImageDraw
import requests
import interactions.ext.files

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
    name="speechbubble",
    description="give it a link to a png image and it will make a speech bubble with it",
    scope=582644566641999874,
    options=[
      interactions.Option(
        name="make",
        description="make a speech bubble",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="url",
            description="image url",
            type=interactions.OptionType.STRING,
            required=True)]),
      interactions.Option(
        name="add",
        description="member to add to the whitelist",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="member",
            description="member to add to the whitelist",
            type=interactions.OptionType.USER,
            required=True)]),
      interactions.Option(
        name="remove",
        description="member to remove from the whitelist",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="member",
            description="member to remove from the whitelist",
            type=interactions.OptionType.USER,
            required=True)]),
      interactions.Option(
        name="list",
        description="shows a list of whitelisted people",
        type=interactions.OptionType.SUB_COMMAND)])
  async def speechbubble(self, ctx: interactions.CommandContext, sub_command, member: str = None, url: str = None):
    f = open(f"speechbubblewhitelist.txt", "r")
    new = str(f.read()).rsplit("\n")
    if sub_command == "make":
      f = open("speechbubblewhitelist.txt", "r")
      new = str(f.read()).rsplit("\n")
      if str(ctx.author.id) not in new:
        await ctx.send(f":x: You are not whitelisted", ephemeral=True)
        f.close()
        return
      if str(ctx.author.id) in new:
        image = Image.open(requests.get(url, stream=True).raw)
        draw = ImageDraw.Draw(image)
        num = list(image.size)
        n1 = ((num[0]/2)+num[0]/4)
        n3 = num[0]/2+num[0]/7
        n4 = num[1]/2
        draw.polygon(((n1, -(num[1]/4)), (n3, n4-(num[1]/4)), (num[0], -(num[1]/16))), fill=0)
        draw.ellipse((0, -(num[1]/16), num[0], (num[1]/16)), fill=0)
        image.save("blank.gif")
        file = interactions.File("blank.gif")
        embed = interactions.Embed()
        embed.set_image(url="attachment://blank.gif")
        await ctx.author.send(embeds=embed, files=file)
        await ctx.send(":white_check_mark: Done! Sent the speech bubble to your DMs; if you have them closed, open them and try again", ephemeral=True)
    if sub_command == "add":
      if 582646886696091669 not in ctx.author.roles:
        await ctx.send(":x: You are not staff!", ephemeral=True)
        return
      if 582646886696091669 in ctx.author.roles:
        if str(member.id) in new:
          await ctx.send(f":x: Error! {member.mention} is already whitelisted!", ephemeral=True)
          f.close()
          return
        if str(member.id) not in new:
          b = open(f"speechbubblewhitelist.txt", "a")
          b.writelines([str(member.id), "\n"])
          await ctx.send(f":white_check_mark: Done! Added {member.mention} to the whitelist!", ephemeral=True)
    if sub_command == "remove":
      if 582646886696091669 not in ctx.author.roles:
        await ctx.send(":x: You are not staff!", ephemeral=True)
        return
      if 582646886696091669 in ctx.author.roles:
        if str(member.id) not in new:
          await ctx.send(f":x: Error! {member.mention} is not whitelisted!", ephemeral=True)
          return
        if str(member.id) in new:
          with open(f"speechbubblewhitelist.txt", "r") as f:
            lines = f.readlines()
          with open(f"speechbubblewhitelist.txt", "w") as f:
            for line in lines:
              if line.strip("\n") != str(member.id):
                f.write(line)
          await ctx.send(f":white_check_mark: Done! Removed {member.mention} from the whitelist!", ephemeral=True)
    if sub_command == "list":
      if 582646886696091669 not in ctx.author.roles:
        await ctx.send(":x: You are not staff!", ephemeral=True)
        return
      if 582646886696091669 in ctx.author.roles:
        new.pop()
        array = []
        for user in new:
          array.append(f"<@!{user}>")
        fuck = "\n".join(array)
        await ctx.send(f"List of people whitelisted:\n\n{fuck}", ephemeral=True)
  
  @interactions.extension_command(
    name="warn",
    description="Warns an user",
    scope=582644566641999874,
    options=[
      interactions.Option(
        name="member",
        description="Member to warn",
        type=interactions.OptionType.USER,
        required=True),
      interactions.Option(
        name="reason",
        description="Warn reason",
        type=interactions.OptionType.STRING,
        requred=True)])
  async def warn(self, ctx: interactions.CommandContext, member, reason):
    if ("1091554735754055790" in str(ctx.author.roles)) or ("582646885265833984" in str(ctx.author.roles)):
      serverembed = interactions.Embed(
        title="Warn",
        description=f"{member.mention} **has been warned by** {ctx.author.mention}\n**Reason:** {reason}",
        color=int(hex(int("FF0000".replace("#", ""), 16)), 0))
      serverembed.set_footer(text="United Corporation Governance Tournaments", icon_url="https://cdn.discordapp.com/icons/582644566641999874/565572bdb6c2c4cc6311f44623ef65a1.png")
      userembed = interactions.Embed(
        title="Warn",
        description=f"**You have been warned by {ctx.author.mention} in UCGT**\n**Reason:** {reason}",
        color=int(hex(int("FF0000".replace("#", ""), 16)), 0))
      userembed.set_footer(text="United Corporation Governance Tournaments", icon_url="https://cdn.discordapp.com/icons/582644566641999874/565572bdb6c2c4cc6311f44623ef65a1.png")
      await ctx.send(embeds=serverembed)
      await ctx.author.send(embeds=userembed)
      return
    if not ("1091554735754055790" in str(ctx.author.roles)) or ("582646885265833984" in str(ctx.author.roles)):
      await ctx.send(":x: You are not a <@&1091554735754055790>", ephemeral=True)
      return

  @interactions.extension_listener()
  async def on_ready(penis):
    print("random has been loaded") 

def setup(bot):
  randomfile(bot)