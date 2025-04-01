import discord
from discord.ext import commands
from discord import app_commands
from cogs.Coins import load_user_data
from models.BlackJackModel import BlackjackGame
from views.BlackJackView import BlackjackView
from logger.logger import JackBotLogger

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = JackBotLogger._instance

    @app_commands.command(name="blackjack", description="Play a game of Blackjack with a bet!")
    @app_commands.describe(bet="The amount you want to bet")
    async def blackjack(self, interaction: discord.Interaction, bet: int):
        """Starts a Blackjack game with the user and a specified bet"""
        self.logger.log_info(f"Blackjack command invoked by {interaction.user.name}({interaction.user.id}) with bet: {bet}")
        user_id = str(interaction.user.id)
        user_data = load_user_data()
        
        if user_id not in user_data:
            await interaction.response.send_message("You need to opt in first! Use /opt to start earning coins.")
            return
        
        if bet <= 0:
            await interaction.response.send_message("You must place a valid bet greater than 0.")
            return

        if bet > user_data[user_id]["coins"]:
            await interaction.response.send_message(f"You don't have enough coins to bet {bet} coins!")
            return

        # Create the game instance
        game = BlackjackGame(bet)

        # Create the view for the game
        view = BlackjackView(interaction, game)

        # Send the initial game message
        content = f"**Welcome to Blackjack!**\nYour Hand: **{', '.join(game.player_hand)}**\n"
        content += f"Dealer's Hand: **{game.dealer_hand[0]}** and [Hidden]\nYou placed a bet of {bet}."
        message = await interaction.response.send_message(content, view=view)

        # Set the message in the view
        view.message = message

async def setup(bot):
    await bot.add_cog(Blackjack(bot))