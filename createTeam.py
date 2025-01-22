import discord
from discord.ui import Button, View

async def create_role(ctx, role_name: str):
    role_color = discord.Color.random()  
    role = await ctx.guild.create_role(name=role_name, color=role_color)

    permissions = discord.Permissions(
        send_messages=True, 
        read_messages=True, 
        connect=True,   
        speak=True     
    )
    await role.edit(permissions=permissions)

    return role

async def create_category(ctx, team_name: str):
    guild = ctx.guild
    category = await guild.create_category(team_name)
    team_role = discord.utils.get(guild.roles, name=team_name)
    
    general_channel = await guild.create_text_channel("general", category=category)
    programming_channel = await guild.create_text_channel("programming", category=category)
    artist_channel = await guild.create_text_channel("artist", category=category)
    voice_channel = await guild.create_voice_channel("voice", category=category)
    await category.set_permissions(team_role, read_messages=True, send_messages=True)
    await general_channel.set_permissions(team_role, read_messages=True, send_messages=True)
    await programming_channel.set_permissions(team_role, read_messages=True, send_messages=True)
    await artist_channel.set_permissions(team_role, read_messages=True, send_messages=True)
    await voice_channel.set_permissions(team_role, connect=True, speak=True)

    return category

async def join_button_callback(interaction: discord.Interaction, team_name: str):
    role = discord.utils.get(interaction.guild.roles, name=team_name)
    if not role:
        await interaction.response.send_message(f"Sorry, the team '{team_name}' does not exist.", ephemeral=True)
        return

    if role in interaction.user.roles:
        await interaction.response.send_message(f"You are already a member of the **{team_name}** team!", ephemeral=True)
    else:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You've successfully joined the **{team_name}** team!", ephemeral=True)

async def leave_button_callback(interaction: discord.Interaction, team_name: str):
    role = discord.utils.get(interaction.guild.roles, name=team_name)
    if not role:
        await interaction.response.send_message(f"Sorry, the team '{team_name}' does not exist.", ephemeral=True)
        return

    if role not in interaction.user.roles:
        await interaction.response.send_message(f"You are not a member of the **{team_name}** team.", ephemeral=True)
    else:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f"You've successfully left the **{team_name}** team.", ephemeral=True)


async def create_interaction_message(ctx, team_name: str):
    role = discord.utils.get(ctx.guild.roles, name=team_name)
    embed = discord.Embed(
        title=f"Join {team_name} Team!",
        description=f"Click the buttons below to join or leave the **{team_name}** team.",
        color=role.color
    )

    join_button = Button(label=f"Join {team_name}", style=discord.ButtonStyle.green, custom_id=f"join_{team_name}")
    join_button.callback = lambda interaction: join_button_callback(interaction, team_name)
   
    leave_button = Button(label=f"Leave {team_name}", style=discord.ButtonStyle.red, custom_id=f"leave_{team_name}")
    leave_button.callback = lambda interaction: leave_button_callback(interaction, team_name)

    view = View()
    view.add_item(join_button)
    view.add_item(leave_button)

    message = await ctx.send(embed=embed, view=view)
    await message.pin()

    return message

   
    

    
