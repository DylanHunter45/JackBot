import os
import asyncio
import discord
import logging
from logger.logger import JackBotLogger
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

logger = JackBotLogger(log_file_path="jackbot.log", log_level=logging.INFO)
logger.log_info("Bot is starting...")

BETA_COGS = ['BlackJack.py']
INCLUDE_BETA_COGS = False

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            if filename in BETA_COGS and not INCLUDE_BETA_COGS:
                logger.log_info(f'{filename} is a beta cog and will not be loaded.')
                continue
            await bot.load_extension(f'cogs.{filename[:-3]}')
            logger.log_info(f'{filename} has been loaded!')

async def main():
    await load()
    await bot.start(token)

asyncio.run(main())