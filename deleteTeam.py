from save import save_server_data, load_server_data
import discord
import os
import json

async def delete_server_data(guild_id, team_name):
    server_data = load_server_data(guild_id)
    
    if team_name in server_data:
        del server_data[team_name]

        server_file = os.path.join("server_data", f"server_data_{guild_id}.json")
        with open(server_file, 'w') as f:
            json.dump(server_data, f, indent=4)
        
    else:
        print(f"Team {team_name} not found in the server data.")

async def delete_server_team(ctx, team_name: str):
    server_data = load_server_data(ctx.guild.id)
    
    if team_name not in server_data:
        await ctx.send(f"No team found with the name '{team_name}'.")
        return

    data = server_data[team_name]
    role_id = data["role_id"]
    category_id = data["category_id"]
    message_id = data["interaction_message"]["message_id"]
    channel_id = data["interaction_message"]["channel_id"]

    role = discord.utils.get(ctx.guild.roles, id=role_id)
    if role:
        await role.delete()
    else:
        await ctx.send(f"Role with ID {role_id} not found.")
        return

    category = discord.utils.get(ctx.guild.categories, id=category_id)
    if category:
        for channel in category.channels:
            await channel.delete()

        await category.delete()
    else:
        await ctx.send(f"Category with ID {category_id} not found.")
        return

    channel = ctx.guild.get_channel(channel_id)
    if channel:
            message = await channel.fetch_message(message_id)
            await message.delete()
    else:
        await ctx.send(f"Channel with ID {channel_id} not found.")
    
    await delete_server_data(ctx.guild.id, team_name)

    await ctx.send(f"The **{team_name}** team has been successfully deleted.")



