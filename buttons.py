import interactions
from interactions import Button, ButtonStyle

class buttons(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot

  tcconfirm = Button(
  style=ButtonStyle.DANGER,
  label="TC confirm",
  custom_id="tcconfirm")

  tcdeny = Button(
  style=ButtonStyle.SECONDARY,
  label="TC cancel",
  custom_id="tcdeny")

  staffconfirm = Button(
  style=ButtonStyle.PRIMARY,
  label="Staff confirm",
  custom_id="staffconfirm")

  staffdeny = Button(
  style=ButtonStyle.SECONDARY,
  label="Staff deny",
  custom_id="staffdeny")
  
  ticket = Button(
  label="Ticket",
  custom_id="ticket",
  style=interactions.ButtonStyle.PRIMARY)

  ticketdelconfirm = Button(
  label="Yes!",
  custom_id="ticketdelconfirm",
  style=interactions.ButtonStyle.SUCCESS)

  ticketdelcancel = Button(
  label="no.",
  custom_id="ticketdelcancel",
  style=interactions.ButtonStyle.DANGER)

  ticketclose = Button(
  label="Ticket Close",
  custom_id="ticketclose",
  style=interactions.ButtonStyle.DANGER)

  resultconfirm = Button(
  style=ButtonStyle.PRIMARY,
  label="Confirm",
  custom_id="resultconfirm")

  resultcancel = Button(
  style=ButtonStyle.DANGER,
  label="Cancel",
  custom_id="resultcancel")

  rules = Button(
    style=ButtonStyle.LINK,
    label="Rules Document",
    url="https://docs.google.com/document/d/1MVyynGQ0xiANmAQtohcPDEH710UrrgTNzn8oEhmgr3k/edit?usp=sharing")

  roledelconfirm = Button(
  style=ButtonStyle.SUCCESS,
  label="Confirm",
  custom_id="roledelconfirm")

  roledelcancel = Button(
  style=ButtonStyle.DANGER,
  label="Cancel",
  custom_id="roledelcancel")

  @interactions.extension_listener()
  async def on_ready(penis):
    print("buttons has been loaded")

def setup(bot):
  buttons(bot)