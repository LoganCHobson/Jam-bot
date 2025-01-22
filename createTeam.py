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

async def create_interaction_message(ctx, team_name: str):
    role = discord.utils.get(ctx.guild.roles, name=team_name)

    async def join_button_callback(interaction: discord.Interaction):
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You've joined {team_name}!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Role {team_name} not found!", ephemeral=True)

    async def leave_button_callback(interaction: discord.Interaction):
        if role:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You've left {team_name}!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Role {team_name} not found!", ephemeral=True)

    join_button = Button(label=f"Join {team_name}", style=discord.ButtonStyle.green, custom_id=f"join_{team_name}")
    join_button.callback = join_button_callback
   
    leave_button = Button(label=f"Leave {team_name}", style=discord.ButtonStyle.red, custom_id=f"leave_{team_name}")
    leave_button.callback = leave_button_callback

    view = View()
    view.add_item(join_button)
    view.add_item(leave_button)

    await ctx.send(f"Click here to join or leave {team_name}", view=view)

   
    

    
