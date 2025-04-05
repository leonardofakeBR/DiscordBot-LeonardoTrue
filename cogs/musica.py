import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque
from Funções.musica.play import play
from Funções.musica.exit import exit
from Funções.musica.pause import pause
from Funções.musica.resume import resume
from Funções.musica.skip import skip

class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name = "play", description = "Toque alguma coisa ,-,")
    async def slash_play(self, interaction:discord.Interaction, musica:str, loop:bool):
        await play(self, interaction, musica, loop)
        
    @app_commands.command(name="skip", description="Pula esse trem ,-,")
    async def slash_skip(self, interaction: discord.Interaction):
        await skip(interaction)

    @app_commands.command(name="pause", description="Quer pausar ?_?")
    async def slash_pause(self, interaction: discord.Interaction):
        await pause(interaction)


    @app_commands.command(name="resume", description="Bora continuar ._.")
    async def slash_resume(self, interaction:discord.Interaction):
        await resume(interaction)


    @app_commands.command(name="exit", description="Quer privacidade é?")
    async def slash_exit(self, interaction:discord.Interaction):
        await exit(interaction)

async def setup(bot):
    await bot.add_cog(Musica(bot))
