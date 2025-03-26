import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.command(aliases=['auth', 'creator', 'about'])
async def author(ctx):
    embed = discord.Embed(title="Who Made Me?", description="This bot was created by alkaliiiscool", color=0x00ff00)
    embed.set_author(name="alkaliiiscool", icon_url=ctx.author.avatar)
    embed.set_thumbnail(url=ctx.author.avatar)
    embed.set_footer(text="Thank you for using this bot!")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(token=token)