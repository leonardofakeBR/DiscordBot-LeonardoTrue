import discord
from discord import app_commands

class LeonardoTrue(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix = ",", intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
    
    async def on_ready(self):
        print(f"{self.user} Ta On")

bot = LeonardoTrue()

@bot.tree.command(name = "hello", description = "Primeiro comando ,-,")
async def hello(interaction:discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}")

@bot.tree.command(name = "soma", description = "Matematica basica ,-,")
@app_commands.describe(
    num1 = "Primeiro número",
    num2 = "Segundo número"
)
async def soma(interaction:discord.Interaction, num1:int, num2:int):
    await interaction.response.send_message(f"A soma de {num1} e {num2} é {num1+num2} burro 0-0")

