import interactions
import discord
import buttons
from buttons import buttons

class tickets(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  ticketmodal = interactions.Modal(
    title="Ticket reason",
    custom_id="ticketmodal",
    components=[
      interactions.TextInput(custom_id="7", style=interactions.TextStyleType.PARAGRAPH, label="Ticket reason", placeholder="Ex: Creating a duo for tournament", min_length=1, max_length=200)])

  @interactions.extension_command(
    name="ticket",
    description="ticket options",
    scope=582644566641999874,
    options=[
        interactions.Option(
        name="channel",
        description="gui channel",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="channel",
            description="gui channel",
            type=interactions.OptionType.CHANNEL,
            required=True)]),
        interactions.Option(
            name="create",
            description="Creates a ticket",
            type=interactions.OptionType.SUB_COMMAND),
        interactions.Option(
            name="close",
            description="Closes a ticket",
            type=interactions.OptionType.SUB_COMMAND),
        interactions.Option(
            name="clean",
            description="Cleans finished tickets",
            type=interactions.OptionType.SUB_COMMAND)])
  async def ticket(self, ctx: interactions.CommandContext, sub_command: str, channel: str = None):
    if sub_command == "channel":
      if "582646886696091669" not in str(ctx.author.roles):
        await ctx.send(":x: You are not a <@&582646886696091669>", ephemeral=True)
        return
      embed = interactions.Embed(
      title="Create a ticket",
      description="Tickets can be used to ask questions directly to staff or to create/join a team during a tournament registration period",
      color=int(hex(int("586ce4".replace("#", ""), 16)), 0))
      embed.set_footer(text="United Corporation Governance Tournaments", icon_url="https://cdn.discordapp.com/icons/582644566641999874/565572bdb6c2c4cc6311f44623ef65a1.png")
      await channel.send(embeds=embed, components=buttons.ticket)
      await ctx.send(f":white_check_mark: Done! Send a ticket GUI to {channel.mention}", ephemeral=True)
    if sub_command == "create":
      await ctx.popup(tickets.ticketmodal)
    elif sub_command == "close":
      if str(ctx.channel.parent_id) not in str(694390326911303723):
        await ctx.send(":x: You are not in a ticket channel!", ephemeral=True)
        return
      try: await ctx.guild.modify_channel(channel_id=int(ctx.channel.id), parent_id=962455110150144100)
      except: await ctx.guild.modify_channel(channel_id=int(ctx.channel.id), parent_id=1007090636274552842)
      await ctx.send(f"Ticket closed by {ctx.author.mention}\n\n:warning: Sending any message in this channel will re-open this ticket!")
      return
    elif sub_command == "clean":
        Staff = discord.utils.find(lambda r: r.id == 582646886696091669, ctx.guild.roles)
        if Staff.id in ctx.author.roles:
            await ctx.send(":warning: **YOU ARE ABOUT TO DELETE ALL FINISHED TICKETS; ARE YOU SURE YOU WANT TO PROCEED?**", components=[buttons.ticketdelconfirm, buttons.ticketdelcancel], ephemeral=True)
        if Staff.id not in ctx.author.roles:
            await ctx.send(f":x: You are not a {Staff.mention} member!", ephemeral=True)

  @interactions.extension_component(buttons.ticket.custom_id)
  async def ticketbutton_response(self, ctx: interactions.CommandContext):
    await ctx.popup(tickets.ticketmodal)

  @interactions.extension_modal("ticketmodal")
  async def ticketmodal_response(self, ctx: interactions.CommandContext, one):
    ticketchannel = await ctx.guild.create_channel(
        f'{ctx.author.name}', interactions.ChannelType.GUILD_TEXT, parent_id=694390326911303723, topic=f"Ticket created by {ctx.author} | (Creator ID: {ctx.author.id})", permission_overwrites=[
            interactions.Overwrite(id=str(ctx.author.id), type=1, allow=interactions.Permissions.VIEW_CHANNEL | interactions.Permissions.SEND_MESSAGES | interactions.Permissions.EMBED_LINKS | interactions.Permissions.ATTACH_FILES),
            interactions.Overwrite(id=str(582646886696091669), type=0, allow=interactions.Permissions.VIEW_CHANNEL | interactions.Permissions.SEND_MESSAGES | interactions.Permissions.EMBED_LINKS | interactions.Permissions.ATTACH_FILES | interactions.Permissions.MANAGE_CHANNELS | interactions.Permissions.MANAGE_ROLES | interactions.Permissions.MENTION_EVERYONE),
            interactions.Overwrite(id=str(582644566641999874), type=0, deny=interactions.Permissions.VIEW_CHANNEL)])
    ticketmessage = await ticketchannel.send(f"Thanks for creating a ticket, {ctx.author.mention}\n\nTicket reason: **{one}**\n\nPlease do not ping any staff members, we will get back to you as soon as possible", components=buttons.ticketclose)
    await ticketchannel.pin_message(ticketmessage)
    await ticketchannel.send("Pssst! Trying to create/join a team/trio/duo? Type `/request` and check out the commands (read their name and description)")
    await ctx.send(f"Ticket created: {ticketchannel.mention}", ephemeral=True)

  @interactions.extension_component(buttons.ticketclose.custom_id)
  async def tickeclosebutton_response(self, ctx: interactions.CommandContext):
    if str(ctx.channel.parent_id) in str(962455110150144100):
        await ctx.send("This ticket was already closed!", ephemeral=True)
    if str(ctx.channel.parent_id) not in str(962455110150144100):
        await ctx.send(f"Ticket closed by {ctx.author.mention}\n\n:warning: Sending any message in this channel will re-open this ticket!")
        try: await ctx.guild.modify_channel(channel_id=int(ctx.channel.id), parent_id=962455110150144100)
        except: await ctx.guild.modify_channel(channel_id=int(ctx.channel.id), parent_id=1007090636274552842)

  @interactions.extension_component(buttons.ticketdelconfirm.custom_id)
  async def delconfirmbutton_response(self, ctx: interactions.CommandContext):
    channel = await ctx.guild.get_all_channels()
    for channel in list(ctx.guild.channels):
      if str(channel.parent_id) in ["962455110150144100", "1007090636274552842"]:
        await channel.delete()
    await ctx.edit(components=[])
    await ctx.send(":white_check_mark: Done deleting all finished tickets!", ephemeral=True)
    staffchannel = discord.utils.find(lambda r: r.id == 704606362218266664, ctx.guild.channels)
    await staffchannel.send(f"{ctx.author.mention} has deleted all finished tickets!")

  @interactions.extension_component(buttons.ticketdelcancel.custom_id)
  async def delcancelbutton_response(self, ctx: interactions.CommandContext):
    await ctx.edit(components=[])
    await ctx.send(":white_check_mark: Action cancelled!", ephemeral=True)

  @interactions.extension_listener()
  async def on_message_create(self, ctx: interactions.Message):
    if ctx.author.id == 1000965619530866760:
      return
    else:
      channel = await ctx.get_channel()
      if str(ctx.author.id) in str(channel.topic):
        if str(channel.parent_id) in ["962455110150144100", "1007090636274552842"]: 
          await channel.modify(parent_id=694390326911303723)
          await channel.send(f"{ctx.author.mention} sent a message and re-opened the ticket!\n\nTo close this ticket, click the button on the pinned message")

  @interactions.extension_listener()
  async def on_ready(penis):
    print("tickets has been loaded") 

def setup(bot):
  tickets(bot)