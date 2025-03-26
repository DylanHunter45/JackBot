import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

bot.run(os.getenv("TOKEN"))