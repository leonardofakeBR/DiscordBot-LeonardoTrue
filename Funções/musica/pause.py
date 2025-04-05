import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque

async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if voice_client is None:
        return await interaction.response.send_message("Nun to no canal, me deixa participar ;-;")

    # Check if something is actually playing
    if not voice_client.is_playing():
        return await interaction.response.send_message("Ta pausando o nada trem? -_-")
    
    # Pause the track
    voice_client.pause()
    await interaction.response.send_message("Cabo a alegria, pausamo ,-,")