import discord
from discord.ext import commands
import os
from createTeam import create_role, create_category, create_interaction_message, join_button_callback, leave_button_callback
from deleteTeam import delete_server_team
from save import save_server_data, load_server_data
from archiveTeam import archive_jam_team, configure_jam_archive

intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True
intents.reactions = True
intents.members = True
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def create_team(ctx, *, team_name: str = ""):

    if team_name == "":
        await ctx.send("Please provide a team name.")
        return
    
    
    existing_role = discord.utils.get(ctx.guild.roles, name=team_name)
    if existing_role:
        await ctx.send(f"A team with the name '{team_name}' already exists.")
        return

    role = await create_role(ctx, team_name)
    
    category = await create_category(ctx, team_name)

    message = await create_interaction_message(ctx, team_name)

    await save_server_data(ctx.guild.id, team_name, message.id, message.channel.id, role.id, category.id)

@bot.command()
async def delete_team(ctx, *, team_name: str = ""):
    if team_name == "":
        await ctx.send("Please provide a team name.")
        return
    
    await delete_server_team(ctx, team_name)

@bot.command()
async def configure_archive_channel(ctx, *, channel: discord.TextChannel):
   
    await configure_jam_archive(ctx, channel)


@bot.command()
async def archive_team(ctx, *, team_name: str = ""):
    if team_name == "":
        await ctx.send("Please provide a team name.")
        return
    
    await archive_jam_team(ctx, team_name)

async def reconstruct_interactions():
    for guild in bot.guilds:
        server_data = load_server_data(guild.id)

        team_data = {k: v for k, v in server_data.items() if k != "archive_channel_id"}

        for team_name, data in team_data.items():
            
            if team_name == "archive_channel_id":
                continue  

           
            if not all(key in data for key in ["role_id", "category_id", "interaction_message"]):
                print(f"Skipping team {team_name} due to missing data")
                continue

            role_id = data["role_id"]
            category_id = data["category_id"]
            interaction_message = data["interaction_message"]

            if not all(key in interaction_message for key in ["message_id", "channel_id"]):
                print(f"Skipping team {team_name} due to missing interaction message data")
                continue

            message_id = interaction_message["message_id"]
            channel_id = interaction_message["channel_id"]

            role = discord.utils.get(guild.roles, id=role_id)
            category = discord.utils.get(guild.categories, id=category_id)

            if role and category:
                channel = guild.get_channel(channel_id)
                if channel:
                    try:
                        message = await channel.fetch_message(message_id)

                        view = discord.ui.View()

                        button1 = discord.ui.Button(label="Join", style=discord.ButtonStyle.green, custom_id=f"join_{team_name}")
                        button2 = discord.ui.Button(label="Leave", style=discord.ButtonStyle.red, custom_id=f"leave_{team_name}")

                        button1.callback = lambda interaction: join_button_callback(interaction, team_name)
                        button2.callback = lambda interaction: leave_button_callback(interaction, team_name)

                        view.add_item(button1)
                        view.add_item(button2)

                        await message.edit(embed=message.embeds[0], view=view)
                    except discord.errors.NotFound:
                        print(f"Message for team {team_name} not found")
                else:
                    print(f"Channel for team {team_name} not found")
            else:
                print(f"Role or category for team {team_name} not found")


@bot.event
async def on_ready():
    
    await reconstruct_interactions()

    print(f'Logged in as {bot.user}')

bot.run(TOKEN)  


