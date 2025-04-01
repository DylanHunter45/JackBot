import discord
from discord.ext import commands
from discord import app_commands
from cogs.BlackJack import BlackjackGame
from cogs.Views.BlackJackView import BlackjackView
import logging
from logger.logger import JackBotLogger

class BlackjackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = JackBotLogger._instance

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
    await bot.add_cog(BlackjackCog(bot))
    logger = JackBotLogger._instance
    logger.info("Blackjack cog has been loaded.")