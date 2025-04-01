import discord
import random
from logger.logger import JackBotLogger
from cogs.Coins import load_user_data, save_user_data

class CoinFlipView(discord.ui.View):
    def __init__(self, user: discord.user, bet: int, message: discord.Message = None):
        super().__init__(timeout=180)
        self.user = user
        self.bet = bet
        self.message = message
        self.logger = JackBotLogger._instance

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.primary)
    async def heads_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.flip_coin(interaction, "Heads")

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.secondary)
    async def tails_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.flip_coin(interaction, "Tails")

    async def flip_coin(self, interaction: discord.Interaction, choice: str):
        self.logger.log_info(f"Coinflip choice made by {interaction.user.name}({interaction.user.id}) with choice: {choice}")
        if interaction.user.id != self.user:
            await interaction.response.send_message("This is not your bet!", ephemeral=True)
            return
        try:
            result = random.choice(["Heads", "Tails"])
            user_id = str(self.user)
            user_data = load_user_data()

            if user_id not in user_data:
                await interaction.response.send_message("You need to opt in first! Use /opt to start earning coins.")
                return

            if choice == result:
                user_data[user_id]["coins"] += self.bet
                await interaction.response.send_message(f"🎉 The coin landed on **{result}**! You won **${self.bet}**! 🥳\nYour new balance: **${user_data[user_id]["coins"]}**") 
            else:
                user_data[user_id]["coins"] -= self.bet
                await interaction.response.send_message(f"😞 The coin landed on **{result}**. You lost **${self.bet}**.\nYour new balance: **{user_data[user_id]["coins"]}**")
        except Exception as e:
            self.logger.log_error(f"Error in coin flip: {e}")
            await interaction.response.send_message("An error occurred while processing your bet. Please try again later.")
        finally:
            save_user_data(user_data)
            self.stop()
            return
        
        
                
