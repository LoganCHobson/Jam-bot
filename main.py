import discord
from discord.ext import commands
import os
from createTeam import create_role, create_category, create_interaction_message

intents = discord.Intents.default()
intents.message_content = True  
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

    await create_role(ctx, team_name)
    
    await create_category(ctx, team_name)

    await create_interaction_message(ctx, team_name)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
   

bot.run(TOKEN)  