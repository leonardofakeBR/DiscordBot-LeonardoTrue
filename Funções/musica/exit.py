import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque

from Funções.global_vars import songs_queues, now_music

async def exit(interaction:discord.Interaction):
    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if not voice_client or not voice_client.is_connected():
        return await interaction.response.send_message("Tá querendo me humilhar é, ja to excluido e quer me tirar ainda ;-;")

    # Clear the guild's queue
    guild_id_str = str(interaction.guild_id)
    if guild_id_str in songs_queues:
        songs_queues[guild_id_str].clear()
        now_music[guild_id_str] = 0

    # If something is playing or paused, stop it
    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()
        # (Optional) Disconnect from the channel

    await voice_client.disconnect()

    await interaction.response.send_message("Vo deixar vcs sozinho 0-0")