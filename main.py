import os
import asyncio
import discord
import json
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'{filename} has been loaded!')

async def main():
    await load()
    await bot.start(token)

asyncio.run(main())