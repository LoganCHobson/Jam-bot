
import discord
from save import load_server_data, save_server_data
import json
import os
import random
import re

def get_channel_color(channel_name):
    colors = {
        'general': discord.Color.green(),
        'programming': discord.Color.purple(),
        'artist': discord.Color.blue(),
    }
    return colors.get(channel_name.lower(), discord.Color(random.randint(0, 0xFFFFFF)))

def sanitize_personal_info(text):
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[Personal Email]', text)
    
    text = re.sub(r'\b(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b', '[Personal Phone]', text)
    
    text = re.sub(r'\d+\s+[A-Za-z\s]+\s+\d{5}(\s+[A-Z]{2})?', '[Personal Location Information]', text)
    
    text = re.sub(r'\b[A-Z][a-z]+(\s+[A-Z]{2})?\s+\d{5}\b', '[Personal Location Information]', text)
    
    return text

async def archive_jam_team(ctx, team_name, type=None):
    server_id = str(ctx.guild.id) 
    server_data_file_path = f"server_data/server_data_{server_id}.json"  

    if not os.path.exists(server_data_file_path):
        await ctx.send(f"Data file for this server does not exist!")
        return

    with open(server_data_file_path, 'r') as f:
        data = json.load(f)
    
    if team_name not in data and type is None:
        await ctx.send(f"Team '{team_name}' not found!")
        return

    team_data = data.get(team_name, {})
    archive_channel_id = data["archive_channel_id"]["archive_channel_id"]
    category_id = team_data.get("category_id")

    if type == "--any":
        category = discord.utils.get(ctx.guild.categories, name=team_name)
        if not category:
            await ctx.send(f"Couldn't find a category named '{team_name}'.")
            return
    else:
        if not category_id:
            await ctx.send(f"Category information not found for team '{team_name}'!")
            return
        category = discord.utils.get(ctx.guild.categories, id=int(category_id))

    archive_channel = discord.utils.get(ctx.guild.text_channels, id=int(archive_channel_id))

    if not category or not archive_channel:
        await ctx.send(f"Couldn't find the category or archive channel.")
        return

    thread = await archive_channel.create_thread(name=f"{team_name} Archive", type=discord.ChannelType.public_thread)

    for channel in category.text_channels:
        channel_color = get_channel_color(channel.name)
        
        label_embed = discord.Embed(
            title=f"Archives from {channel.name.upper()}",
            color=channel_color,
            description="᲼" 
        )
        label_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        await thread.send(embed=label_embed)

        async for message in channel.history(oldest_first=True):
            
            
            sanitized_content = sanitize_personal_info(message.content) 
            
            embed = discord.Embed(
                description=sanitized_content if message.content else None,
                color=channel_color,
                timestamp=message.created_at
            )
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
            
            if message.attachments:
                files = [await attachment.to_file() for attachment in message.attachments]
                file_message = await thread.send(files=files)
                file_link = f"https://discord.com/channels/{ctx.guild.id}/{thread.id}/{file_message.id}"
                embed.add_field(name="Attachments", value=f"[View Attachments]({file_link})", inline=False)
            
            if embed.description or embed.fields:
                await thread.send(embed=embed)

    await ctx.send(f"Team '{team_name}' has been archived successfully!")



async def configure_jam_archive(ctx, channel: discord.TextChannel):
    file_path = f"server_data/server_data_{ctx.guild.id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            server_data = json.load(f)
    else:
        server_data = {}

    if str(ctx.guild.id) not in server_data:
        server_data[str("archive_channel_id")] = {}

    server_data[str("archive_channel_id")]["archive_channel_id"] = channel.id

    with open(file_path, "w") as f:
        json.dump(server_data, f, indent=4)

    await ctx.send(f"The archive channel has been set to {channel.mention}.")