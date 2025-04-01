import discord
import random
from discord.ext import commands
from discord import app_commands
from views.BlackJackView import BlackjackView
from logger.logger import JackBotLogger

# Card deck for Blackjack
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

class BlackjackGame:
    def __init__(self, bet, deck=None):
        self.bet = bet
        self.deck = deck if deck else self.create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.player_value = self.hand_value(self.player_hand)
        self.dealer_value = self.hand_value(self.dealer_hand)
        self.game_over = False
        self.doubled = False

    def create_deck(self):
        """Returns a shuffled deck of cards"""
        deck = [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]
        random.shuffle(deck)
        return deck

    def hand_value(self, hand):
        """Returns the value of the hand"""
        value = 0
        aces = 0
        for card in hand:
            rank = card.split()[0]
            value += VALUES[rank]
            if rank == 'A':
                aces += 1

        # Adjust for aces (Aces are worth 1 if the total value exceeds 21)
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def dealer_turn(self):
        """The dealer draws until their hand value is at least 17"""
        while self.dealer_value < 17:
            self.dealer_hand.append(self.deck.pop())
            self.dealer_value = self.hand_value(self.dealer_hand)

    def hit(self):
        """Draws a card for the player"""
        self.player_hand.append(self.deck.pop())
        self.player_value = self.hand_value(self.player_hand)

    def double_down(self):
        """Doubles the player's bet and draws a single card"""
        self.doubled = True
        self.bet *= 2
        self.hit()

    def finalize_game(self):
        """Determine the result of the game after the player stands"""
        self.dealer_turn()

        if self.player_value > 21:
            return "bust"
        if self.dealer_value > 21:
            return "dealer_bust"
        if self.player_value > self.dealer_value:
            return "win"
        if self.player_value < self.dealer_value:
            return "dealer_win"
        return "tie"

class Blackjack(commands.Cog):
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
    await bot.add_cog(Blackjack(bot))
    logger = JackBotLogger._instance
    logger.info("Blackjack cog has been loaded.")