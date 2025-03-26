import discord
import os
import json
import datetime
from discord.ext import commands
from discord.ext.commands import Cog

def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as f:
            return json.load(f)
    else:
        with open('user_data.json', 'w') as f:
            json.dump({}, f)
            return {}

def save_user_data(data):
    with open('user_data.json', 'w') as f:
        json.dump(data, f)

def should_claim_daily(user_data):
    today = str(datetime.datetime.now().date())
    if user_data['last_claimed'] != today:
        return True
    return False

def increase_multiplier(user_data):
    today = str(datetime.datetime.now().date())
    yesterday = str(datetime.datetime.now().date() - datetime.timedelta(days=1))
    if user_data['last_claimed'] == yesterday:
        user_data['multiplier'] += 0.1
    else:
        user_data['multiplier'] = 1.0
    user_data['multiplier'] = round(user_data['multiplier'], 1)
    user_data['last_claimed'] = today

class Coins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_data = load_user_data()

    #opt in and start earning coins
    @commands.command(aliases=['opt', 'start'])
    async def opt_in(self, ctx):
        print(f"Opt in called by {ctx.author.name}")
        user_id = str(ctx.author.id)
        if self.user_data is None:
            self.user_data[user_id] = {
                'coins': 0,
                'last_claimed': "",
                'multiplier': 1
            }
            save_user_data(self.user_data)
            await ctx.send(f'{ctx.author.mention} You have opted in! Use .daily to get daily coins and .coins to check your balance!')
        elif user_id not in self.user_data:
            # Opt-in the user and grant 100 coins
            self.user_data[user_id] = {
                'coins': 0,
                'last_claimed': "",
                'multiplier': 1
            }
            save_user_data(self.user_data)
            await ctx.send(f'{ctx.author.mention} You have opted in! Use .daily to get daily coins and .coins to check your balance!')
        else:
            await ctx.send(f'{ctx.author.mention} You are already opted in! Remember to use .coins to check your balance and .daily to earn coins daily!')

    #cheack coin balance
    @commands.command(aliases=['bal', 'money', 'coins', 'balance'])
    async def check_balance(self, ctx):
        print(f"Balance check called by {ctx.author.name}")
        user_id = str(ctx.author.id)
        if user_id not in self.user_data:
            await ctx.send(f'{ctx.author.mention} You are not opted in! Use .opt to start earning coins!')
        else:
            await ctx.send(f'{ctx.author.mention} You have {self.user_data[user_id]["coins"]} coins! Earn more by using .daily, consecutive daily claims will increase your multiplier!')

    #claim daily coins
    @commands.command(aliases=['daily', 'claim'])
    async def claim_daily(self, ctx):
        print(f"Daily claim called by {ctx.author.name}")
        user_id = str(ctx.author.id)
        if user_id not in self.user_data:
            await ctx.send(f'{ctx.author.mention} You are not opted in! Use .opt to start earning coins!')
        else:
            if should_claim_daily(self.user_data[user_id]):
                self.user_data[user_id]['coins'] += (100 * self.user_data[user_id]['multiplier'])
                self.user_data[user_id]['coins'] = round(self.user_data[user_id]['coins'], 1)
                increase_multiplier(self.user_data[user_id])
                save_user_data(self.user_data)
                await ctx.send(f'{ctx.author.mention} You have claimed your daily coins! Use .coins to check your balance!')
            else:
                await ctx.send(f'{ctx.author.mention} You have already claimed your daily coins! Please wait until tomorrow to claim again!')
    
    #check current multiplier
    @commands.command()
    async def multiplier(self, ctx):
        print(f"Multiplier check called by {ctx.author.name}")
        user_id = str(ctx.author.id)
        if user_id not in self.user_data:
            await ctx.send(f'{ctx.author.mention} You are not opted in! Use .opt to start earning coins!')
        else:
            await ctx.send(f'{ctx.author.mention} Your current multiplier is {self.user_data[user_id]["multiplier"]}x!')

    
async def setup(bot):
    await bot.add_cog(Coins(bot))