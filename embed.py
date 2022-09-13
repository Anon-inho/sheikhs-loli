import interactions
from interactions import Modal, Embed
import discord

class embed(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  modale = Modal(
      custom_id="modal",
      title="Build an embed",
      components=[
        interactions.TextInput(custom_id="1", style=interactions.TextStyleType.SHORT, label="Title", placeholder="Title", required=False), 
        interactions.TextInput(custom_id="2", style=interactions.TextStyleType.PARAGRAPH, label="Description", placeholder="Description", required=True),
        interactions.TextInput(custom_id="3", style=interactions.TextStyleType.SHORT, label= "Footer", placeholder="Footer", required=False),
        interactions.TextInput(custom_id="4", style=interactions.TextStyleType.SHORT, label="Color", placeholder="Color in hex (Ex: 123456)", required=True)])

  @interactions.extension_command(
    name="embed",
    description="Builds an embed",
    scope=582644566641999874,
    default_member_permissions=interactions.Permissions.MANAGE_CHANNELS,
    options=[
      interactions.Option(
        name="channel",
        description="Channel to send the embed to",
        type=interactions.OptionType.CHANNEL,
        required=False)])
  async def embed(self, ctx: interactions.CommandContext, channel: str = None):
    if channel == None:
      channel = ctx.channel
    await ctx.popup(embed.modale)
    global channelglobal
    channelglobal = channel

  @interactions.extension_modal("modal")
  async def modal(self, ctx: interactions.CommandContext, one, two, three, four):
    readableHex = int(hex(int(four.replace("#", ""), 16)), 0)
    embed = Embed(title=one, description=two, color=readableHex)
    embed.set_footer(three)
    channel = discord.utils.find(lambda r: r.id == channelglobal.id, ctx.guild.channels)
    await channel.send(embeds=embed)
    await ctx.send(f":white_check_mark: Embed sent to {channelglobal.mention}", ephemeral=True)

  @interactions.extension_listener()
  async def on_ready(penis):
    print("embed has been loaded") 

def setup(bot):
  embed(bot)