import discord
from discord import app_commands
from discord.ext import commands

from Funções.global_vars import songs_queues, now_music

async def loop(interaction:discord.Interaction):

    guild_id = str(interaction.guild_id)
    audio_url, title, loop = songs_queues[guild_id][0]
    songs_queues[guild_id][0] = (audio_url, title, not loop)

    if loop:
        now_music[guild_id] -= 1
        await interaction.response.send_message(f"{title} agora está em loop ,-,")
        
    else:
        now_music[guild_id] += 1
        await interaction.response.send_message(f"{title} não está mais em loop ,-,")