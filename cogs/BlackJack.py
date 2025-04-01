import discord
from discord.ext import commands
from discord import app_commands
from models.BlackJackModel import BlackjackGame
from views.BlackJackView import BlackjackView
from logger.logger import JackBotLogger

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="blackjack", description="Play a game of Blackjack with a bet!")
    async def blackjack(self, interaction: discord.Interaction, bet: int):
        """Starts a Blackjack game with the user and a specified bet"""
        if bet <= 0:
            await interaction.response.send_message("You must place a valid bet greater than 0.")
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