import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")   

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(token=token)