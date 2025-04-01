import discord
from discord.ext import commands
from discord import app_commands
from models.BlackJackModel import BlackjackGame

class BlackjackView(discord.ui.View):
    def __init__(self, interaction, game: BlackjackGame):
        super().__init__()
        self.interaction = interaction
        self.game = game
        self.message = None

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.game.game_over:
            self.game.hit()
            await self.update_message(interaction)
            if self.game.player_value > 21:
                await self.finalize_game(interaction, "bust")

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.success)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.game.game_over:
            result = self.game.finalize_game()
            await self.finalize_game(interaction, result)

    @discord.ui.button(label="Double Down", style=discord.ButtonStyle.danger)
    async def double(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.game.doubled and len(self.game.player_hand) == 2:
            self.game.double_down()
            await self.update_message(interaction)
            if self.game.player_value > 21:
                await self.finalize_game(interaction, "bust")

    @discord.ui.button(label="Split", style=discord.ButtonStyle.secondary)
    async def split(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Implement splitting functionality here if needed
        pass

    async def update_message(self, interaction: discord.Interaction):
        """Updates the game status message"""
        content = f"Your Hand: **{', '.join(self.game.player_hand)}** (Value: {self.game.player_value})\n"
        content += f"Dealer's Hand: **{', '.join(self.game.dealer_hand)}** (Value: {self.game.dealer_value})"
        if self.game.player_value > 21:
            content += "\n**You busted!**"
        if self.game.dealer_value > 21:
            content += "\n**Dealer busted!**"
        if self.message:
            await self.message.edit(content=content)

    async def finalize_game(self, interaction: discord.Interaction, result: str):
        """Finalizes the game and sends the result"""
        if self.game.game_over:
            return

        self.game.game_over = True
        if result == "bust":
            content = f"**You busted!** Dealer wins. You lost {self.game.bet}."
        elif result == "dealer_bust":
            content = f"**Dealer busted!** You win! You earned {self.game.bet}."
        elif result == "win":
            content = f"**You win!** You earned {self.game.bet}."
        elif result == "dealer_win":
            content = f"**Dealer wins!** Better luck next time. You lost {self.game.bet}."
        elif result == "tie":
            content = "**It's a tie!** No one wins or loses."

        await self.message.edit(content=content)
        self.stop()