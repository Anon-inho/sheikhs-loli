from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import interactions
import discord
from buttons import buttons

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1MVyynGQ0xiANmAQtohcPDEH710UrrgTNzn8oEhmgr3k'

creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
service = build('docs', 'v1', credentials=creds)
document = service.documents().get(documentId=DOCUMENT_ID).execute()

heading1 = ""
heading2 = ""
rulesjson = {}
choicearray = []
deck = []
title = document.get('body')
for i in range(1, len(title['content'])):
  text = str(title['content'][i]['paragraph']['elements'][0]['textRun']['content']).replace("\n", "")
  type = str(title['content'][i]['paragraph']['paragraphStyle']['namedStyleType']).replace("\n", "")
  try: 
    if type == "HEADING_2":
      heading1 = text
      rulesjson[heading1] = {}
      rulesjson[heading1]['information'] = []
      choicearray.append(
      interactions.Choice(
        name=text, 
        value=text))
      deck.append(text)
    if type == "NORMAL_TEXT":
      rulesjson[heading1]['information'].append(text)
  except:
    continue

class docs(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  @interactions.extension_command(
    name="rules",
    description="see rules",
    scope=582644566641999874,
    options=[
      interactions.Option(
        name="topic",
        description="rule topic",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="topic",
            description="rule topic",
            type=interactions.OptionType.STRING,
            required=True,
            choices=choicearray)]),
      interactions.Option(
        name="all",
        description="sends all rules",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="channel",
            description="where you want to send rules to",
            type=interactions.OptionType.CHANNEL,
            required=True)])])
  async def rules(self, ctx: interactions.CommandContext, sub_command: str = None, topic: str = None, channel: str = None):
    if sub_command == "topic":
      embed = interactions.Embed(
        title=topic,
        description=str("\n".join(rulesjson[topic]['information'])).replace("[", "").replace("]", ""),
        color=5471228)
      await ctx.send(embeds=embed, components=buttons.rules)
    if sub_command == "all":
      if "582646886696091669" not in str(ctx.author.roles):
        await ctx.send(":x: You are not a staff member. To read all rules, head over to <#586382177751531540>", ephemeral=True)
      if "582646886696091669" in str(ctx.author.roles):
        currentchannel = discord.utils.find(lambda r: r.id == int(ctx.channel.id), ctx.guild.channels)
        var = []
        for item in deck:
          embed = interactions.Embed(
            title=item,
            description=str("\n".join(rulesjson[item]['information'])).replace("[", "").replace("]", ""),
            color=5471228)
          sendchannel = discord.utils.find(lambda r: r.id == int(channel.id), ctx.guild.channels)
          var.append("a")
          if len(var) != len(deck):
            await sendchannel.send(embeds=embed)
          if len(var) == len(deck):
            await sendchannel.send(embeds=embed, components=buttons.rules)
            break
        var.clear()
        await currentchannel.send(f":white_check_mark: Done! Sent all rules to {channel.mention}")


  @interactions.extension_listener()
  async def on_ready(penis):
    print("docs has been loaded")

def setup(bot):
  docs(bot)