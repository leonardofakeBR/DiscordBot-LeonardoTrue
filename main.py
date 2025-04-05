import os
from botToken import botToken
import discord
from discord.ext import commands
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "..", intents = intents)

async def carregar_cogs():
    for arquivo in os.listdir("cogs"):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"cogs.{arquivo[:-3]}")

@bot.event
async def on_ready():
    await carregar_cogs()
    await bot.tree.sync()
    print(f"{bot.user} Ta On")

bot.run(botToken._token)
