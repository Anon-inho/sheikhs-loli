import interactions
import discord
import buttons
from buttons import buttons

class confirm(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  @interactions.extension_command(
    name="confirm", 
    description="Proposes a match confirmation", 
    scope=582644566641999874,
    options=[
        interactions.Option(
            name="team",
            description="Proposes a match confirmation for teams",
            type=interactions.OptionType.SUB_COMMAND),
        interactions.Option(
            name="trio",
            description="Proposes a match confirmation for trios",
            type=interactions.OptionType.SUB_COMMAND),
        interactions.Option(
            name="duo",
            description="Proposes a match confirmation for duos",
            type=interactions.OptionType.SUB_COMMAND),
        interactions.Option(
            name="staff",
            description="Forces a match confirmation",
            type=interactions.OptionType.SUB_COMMAND)])
  async def confirm(self, ctx: interactions.CommandContext, sub_command: str):
    if sub_command == "team":
      captainid = 694367677262725212
      category = 1001966433372213409
      placeholder = "4v4"
    if sub_command == "trio":
      captainid = 799846360546541589
      category = 1002353768320466955
      placeholder = "3v3"
    if sub_command == "duo":
      captainid = 703375168801734786
      category = 1001966453089632399
      placeholder = "2v2"
    if sub_command == "staff":
      if "582646886696091669" in str(ctx.author.roles):
        if str(ctx.channel.parent_id) in ["1001966433372213409", "1002353768320466955", "1001966453089632399"]:
          staffmodal = interactions.Modal(
            title="Match confirming",
            custom_id="staffmodal",
            components=[
                interactions.TextInput(custom_id="1", style=interactions.TextStyleType.SHORT, label="Type", placeholder="Ex: Team"),
                interactions.TextInput(custom_id="2", style=interactions.TextStyleType.SHORT, label="Match date", placeholder="Ex: February 30"), 
                interactions.TextInput(custom_id="3", style=interactions.TextStyleType.SHORT, label="Match time in your favored timezone", placeholder="Ex: 2 PM EST"),
                interactions.TextInput(custom_id="4", style=interactions.TextStyleType.SHORT, label="Team size", placeholder="Ex: 4v4")])
          await ctx.popup(staffmodal)
          return
        if str(ctx.channel.parent_id) not in ["1001966433372213409", "1002353768320466955", "1001966453089632399"]:
          await ctx.send(":x: This is not a scheduling channel!", ephemeral=True)
          return
      if "582646886696091669" not in str(ctx.author.roles):
        await ctx.send(":x: You are not a <@&582646886696091669>", ephemeral=True)
        return
    TeamCaptain = discord.utils.find(lambda r: r.id == str(captainid), ctx.guild.roles)
    if TeamCaptain.id in ctx.author.roles:
        if str(ctx.channel.parent_id) in str(category):
            modal = interactions.Modal(
            title="Match confirming",
            custom_id="teamconfirm",
            components=[
                interactions.TextInput(custom_id="1", style=interactions.TextStyleType.SHORT, label="Match date", placeholder="Ex: February 30"), 
                interactions.TextInput(custom_id="2", style=interactions.TextStyleType.SHORT, label="Match time in your favored timezone", placeholder="Ex: 2 PM EST"),
                interactions.TextInput(custom_id="3", style=interactions.TextStyleType.SHORT, label="Team size", placeholder=f"Ex: {placeholder}")])
            await ctx.popup(modal)
    if str(ctx.channel.parent_id) not in str(category):
        await ctx.send(f":x: You must be in a {sub_command} scheduling channel to send this command!", ephemeral=True)
    if TeamCaptain.id not in ctx.author.roles:
        await ctx.send(f":x: You are not a {TeamCaptain.mention}", ephemeral=True)
    global captainidglobal
    captainidglobal = captainid

  @interactions.extension_modal("staffmodal")
  async def staffmodal_response(self, ctx: interactions.CommandContext, one, two, three, four):
    confirmed = await ctx.send(f"Staff has confirmed the {one} match!\n\n**Match date**: {two}\n**Match time**: {three}\n**{one} size**: {four}")
    await ctx.channel.pin_message(confirmed)
    schannel = ctx.channel.id
    nchannel = ctx.channel.name
    staffchannel = discord.utils.find(lambda r: r.id == 1003135348236353576, ctx.guild.channels)
    await staffchannel.send(f"{one} match confirmed by {ctx.author.mention}!\n{nchannel} (<#{schannel}>)\n\n**Match date**: {two}\n**Match time**: {three}\n**{one} size**: {four}")

  @interactions.extension_modal("teamconfirm")
  async def modal_response(self, ctx: interactions.CommandContext, one, two, three):
    await ctx.get_channel()
    await ctx.send(f"{ctx.author.mention} has proposed a schedule!\n\n**Match date**: {one}\n**Match time**: {two}\n**Team size**: {three}", components=[buttons.tcconfirm, buttons.tcdeny])
    await ctx.channel.send("<@&694367677262725212>", allowed_mentions={"parse": ["roles", "users"]})
    firsttc = ctx.author
    global one1global
    global two1global
    global three1global
    global firsttcglobal
    one1global = one
    two1global = two
    three1global = three
    firsttcglobal = firsttc

  @interactions.extension_component(buttons.tcconfirm.custom_id)
  async def tc_button_response(self, ctx: interactions.CommandContext):
    TeamCaptain = discord.utils.find(lambda r: r.id == str(captainidglobal), ctx.guild.roles)
    if TeamCaptain.id in ctx.author.roles:
        if str(firsttcglobal.id) not in str(ctx.author.id):
            await ctx.edit(components=[])
            await ctx.get_channel()
            await ctx.channel.send(f"Both Team Captains have confirmed the match!\n\n**Match date:** {one1global}\n**Match time:** {two1global}\n**Team size:** {three1global}\n\n<@&582646886696091669>, please confirm the match by clicking the button below", components=[buttons.staffconfirm, buttons.staffdeny], allowed_mentions={"parse": ["roles", "users"]})
    if TeamCaptain.id not in ctx.author.roles:
        await ctx.send(f":x: You are not a {TeamCaptain.mention}", ephemeral=True)
    if str(firsttcglobal.id) in str(ctx.author.id):
        await ctx.send(f":x: The other {TeamCaptain.mention} needs to confirm the match", ephemeral=True)

  @interactions.extension_component(buttons.tcdeny.custom_id)
  async def team_deny_response(self, ctx: interactions.CommandContext):
    TeamCaptain = discord.utils.find(lambda r: r.id == str(captainidglobal), ctx.guild.roles)
    if TeamCaptain.id in ctx.author.roles:
        await ctx.edit(components=[])
        await ctx.send(f"{TeamCaptain.mention} has cancelled the proposed scheduling")
    if TeamCaptain.id not in ctx.author.roles:
        await ctx.send(f":x: You are not a {TeamCaptain.mention}", ephemeral=True)

  @interactions.extension_component(buttons.staffconfirm.custom_id)
  async def teamstaff_button_response(self, ctx: interactions.CommandContext):
    Staff = discord.utils.find(lambda r: r.id == 582646886696091669, ctx.guild.roles)
    if Staff.id in ctx.author.roles:
        await ctx.edit(components=[])
        confirmed = await ctx.send(f"Match confirmed!\n\n**Match date:** {one1global}\n**Match time:** {two1global}\n**Team size:** {three1global}")
        await ctx.channel.pin_message(confirmed)
        schannel = ctx.channel.id
        nchannel = ctx.channel.name
        staffchannel = discord.utils.find(lambda r: r.id == 1003135348236353576, ctx.guild.channels)
        await staffchannel.send(f"Team match confirmed by {ctx.author.mention}\n{nchannel} (<#{schannel}>)\n\n**Match date:** {one1global}\n**Match time:** {two1global}\n**Team size:** {three1global}")
    if Staff.id not in ctx.author.roles:
        await ctx.send(f":x: You are not a {Staff.mention}", ephemeral=True)

  @interactions.extension_component(buttons.staffdeny.custom_id)
  async def teamstaffdeny_button_response(self, ctx: interactions.CommandContext):
    Staff = discord.utils.find(lambda r: r.id == 582646886696091669, ctx.guild.roles)
    if Staff.id in ctx.author.roles:
        await ctx.edit(components=[])
        await ctx.send(f"The proposed schedule was denied by {ctx.author.mention}")
    if Staff.id not in ctx.author.roles:
        await ctx.send(f":x: You are not a {Staff.mention}", ephemeral=True)

  @interactions.extension_listener()
  async def on_ready(penis):
    print("confirm has been loaded")
    

def setup(bot):
  confirm(bot)