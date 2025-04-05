import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque

from Funções.global_vars import songs_queues, now_music

async def skip(interaction:discord.Interaction):
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        guild_id = str(interaction.guild_id)
        now_music[guild_id] += 1
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("Pulamo essa aberração 0-0")
    else:
        await interaction.response.send_message("Não da pra pular algo que não existe .-.")