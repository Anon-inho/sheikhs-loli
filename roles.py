import interactions
from buttons import buttons

class roles(interactions.Extension):
  def __init__(self, bot):
    self.bot: interactions.Client = bot
    
  @interactions.extension_command(
    name="transfertc",
    description="yes i have become that lazy leave me alone",
    scope=582644566641999874,
    default_member_permissions=interactions.Permissions.MANAGE_ROLES,
    options=[
      interactions.Option(
        name="size",
        description="which tc to transfer (team/trio/duo)",
        type=interactions.OptionType.ROLE,
        required=True),
      interactions.Option(
        name="currenttc",
        description="user who currently has tc",
        type=interactions.OptionType.USER,
        required=True),
      interactions.Option(
        name="newtc",
        description="user who will be tc",
        type=interactions.OptionType.USER,
        required=True)])
  async def transfertc(self, ctx: interactions.CommandContext, size, currenttc, newtc):
    if str(size.id) not in ["1045752403951104030", "799846360546541589", "703375168801734786"]:
      await ctx.send(":x: Must be a captain role!", ephemeral=True)
      return
    if size.id not in currenttc.roles:
      await ctx.send(f"{currenttc.mention} is not a {size.mention}", ephemeral=True)
      return
    if size.id in newtc.roles:
      await ctx.send(f"{currenttc.mention} is already a {size.mention}", ephemeral=True)
      return
    if currenttc.id == newtc.id:
      await ctx.send(":x: i dont think you can transfer a role from one person to the same person (i wrote this at 1 am idek what im doing anymore please help this is not me complaining this is a cry for help)")
      return
    await currenttc.remove_role(role=size.id, guild_id=582644566641999874)
    await newtc.add_role(role=size.id, guild_id=582644566641999874)
    await ctx.send(f":white_check_mark: Done! Transfered {size.mention} from {currenttc.mention} to {newtc.mention}", ephemeral=True)

  @interactions.extension_command(
    name="role",
    description="do some stuff with roles",
    scope=582644566641999874,
    default_member_permissions=interactions.Permissions.MANAGE_ROLES,
    options=[
      interactions.Option(
        name="create",
        description="create a role",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="under",
            description="under which role do you want this new role to be",
            type=interactions.OptionType.ROLE,
            required=True)]),
      interactions.Option(
        name="delete",
        description="deletes a role",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="role",
            description="role you wait to delete",
            type=interactions.OptionType.ROLE,
            required=True)]),
      interactions.Option(
        name="add",
        description="give a role to someone",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="user",
            description="user you want to add the role",
            type=interactions.OptionType.USER,
            required=True),
          interactions.Option(
            name="role",
            description="role you want to add",
            type=interactions.OptionType.ROLE,
            required=True)]),
      interactions.Option(
        name="remove",
        description="remove a role from someone",
        type=interactions.OptionType.SUB_COMMAND,
        options=[
          interactions.Option(
            name="user",
            description="user you want to remove the role from",
            type=interactions.OptionType.USER,
            required=True),
          interactions.Option(
            name="role",
            description="role you want to remove",
            type=interactions.OptionType.ROLE,
            required=True)])])
  async def role(self, ctx: interactions.CommandContext, sub_command, under: str = None, user: str = None, role: str = None):
    if sub_command == "create":
      modale = interactions.Modal(
      custom_id="modalee",
      title="Build an embed",
      components=[
        interactions.TextInput(custom_id="1", style=interactions.TextStyleType.SHORT, label="Role name", placeholder="name", required=True), 
        interactions.TextInput(custom_id="2", style=interactions.TextStyleType.SHORT, label="Role color (hex)", placeholder="123456", required=True)])
      await ctx.popup(modale)
      global globalunder
      globalunder = under.position
    if sub_command == "add":
      if role.id in user.roles:
        await ctx.send(f":x: {user.mention} already has the {role.mention} role!", ephemeral=True)
        return
      await user.add_role(role=role.id, guild_id=582644566641999874)
      await ctx.send(f":white_check_mark: Done! Added the {role.mention} role to {user.mention}", ephemeral=True)
    if sub_command == "remove":
      if role.id not in user.roles:
        await ctx.send(f":x: {user.mention} does not have the {role.mention} role!", ephemeral=True)
        return
      await user.remove_role(role=role.id, guild_id=582644566641999874)
      await ctx.send(f":white_check_mark: Done! Removed the {role.mention} role from {user.mention}", ephemeral=True)
    if sub_command == "delete":
      await ctx.send(f":warning: **ARE YOU SURE YOU WANT TO DELETE {role.mention}**", components=[buttons.roledelconfirm, buttons.roledelcancel], ephemeral=True)
      global globalrole
      globalrole = role.id

  @interactions.extension_component(buttons.roledelconfirm.custom_id)
  async def roledelconfirm_response(self, ctx: interactions.CommandContext):
    await ctx.guild.delete_role(role_id=globalrole)
    await ctx.send(":white_check_mark: Done! Deleted the role", ephemeral=True)

  @interactions.extension_component(buttons.roledelcancel.custom_id)
  async def roledelcancel_response(self, ctx: interactions.CommandContext):
    await ctx.edit(components=[])
    await ctx.send(":white_check_mark: Action cancelled", ephemeral=True)

  @interactions.extension_modal("modalee")
  async def modale_response(self, ctx: interactions.CommandContext, one, two):
    readableHex = int(hex(int(two.replace("#", ""), 16)), 0)
    role = await ctx.guild.create_role(name=one, color=readableHex)
    await role.modify_position(guild_id=582644566641999874, position=int(globalunder))
    await ctx.send(f":white_check_mark: Done! Created the {role.mention} role!", ephemeral=True)

  @interactions.extension_listener()
  async def on_ready(penis):
    print("roles has been loaded") 

def setup(bot):
  roles(bot)