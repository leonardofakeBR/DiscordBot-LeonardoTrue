import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque

from Funções.global_vars import songs_queues, now_music

async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if voice_client is None:
        return await interaction.response.send_message("Nun to no canal, me deixa participar ;-;")

    # Check if it's actually paused
    if not voice_client.is_paused():
        return await interaction.response.send_message("Ue quer resumir a musica que já ta tocando p_p")
    
    # Resume playback
    voice_client.resume()
    await interaction.response.send_message("Vamo terminar de escutar esse treco !_!")