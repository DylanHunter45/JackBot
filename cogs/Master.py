import discord
from discord.ext import commands
from discord.ext.commands import Cog

class Master(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has connected to Discord!')

    @commands.command(aliases=['auth', 'creator', 'about'])
    async def author(self, ctx):
        embed = discord.Embed(title="Who Made Me?", description="This bot was created by alkaliiiscool", color=0x00ff00)
        embed.set_author(name="alkaliiiscool", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=ctx.author.avatar)
        embed.set_footer(text="Thank you for using this bot!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Master(bot))