import discord
from logger.logger import JackBotLogger
from cogs.Coins import load_user_data, save_user_data
from views import CoinFlipView
from discord import app_commands
from discord.ext import commands

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = JackBotLogger._instance

    @app_commands.command(name="coinflip", description="Flip a coin! Bet some coins and see if you win!")
    @app_commands.describe(bet="The amount you want to bet")
    async def coinflip(self, interaction: discord.Interaction, bet: int):
        """Flip a coin and bet some coins!"""
        self.logger.log_info(f"Coinflip command invoked by {interaction.user.name}({interaction.user.id}) with bet: {bet}")
        user_id = str(interaction.user.id)
        user_data = load_user_data()

        if user_id not in user_data:
            await interaction.response.send_message("You need to opt in first! Use /opt to start earning coins.")
            return

        if user_data[user_id]["coins"] <= 0:
            await interaction.response.send_message("You don't have any coins! Use /daily to earn some coins or trade with a friend to get more.")
            return

        if bet > user_data[user_id]["coins"]:
            await interaction.response.send_message(f"You don't have enough coins to bet {bet} coins!")
            return

        try:
            view = CoinFlipView.CoinFlipView(interaction.user.id, bet)
        except Exception as e:
            self.logger.log_error(f"Error creating CoinFlipView: {e}")
            await interaction.response.send_message("An error occurred while creating the coin flip view. Please try again later.")
            return
        
        await interaction.response.send_message(f"{interaction.user.global_name} is betting ${bet}! Pick Heads or Tails!", view=view)
async def setup(bot):
    await bot.add_cog(CoinFlip(bot))