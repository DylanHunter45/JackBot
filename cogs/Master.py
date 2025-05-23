import discord
import logging
from logger.logger import JackBotLogger 
from discord.ext import commands, tasks
from discord.ext.commands import Cog

class Master(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = JackBotLogger._instance

    @tasks.loop(seconds=15)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(name="use .daily to earn coins!"))

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.log_info(f'{self.bot.user} has connected to Discord!')
        self.change_status.start()
        try:
            sync_commands = await self.bot.tree.sync()
            print(f"{len(sync_commands)} commands registered")
        except Exception as e:
            print(f"An error occurred: {e}")

    @commands.command(aliases=['auth', 'creator', 'about'])
    async def author(self, ctx):
        embed = discord.Embed(title="Who Made Me?", description="This bot was created by alkaliiiscool", color=0x00ff00)
        embed.set_author(name="alkaliiiscool", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=ctx.author.avatar)
        embed.set_footer(text="Thank you for using this bot!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Master(bot))