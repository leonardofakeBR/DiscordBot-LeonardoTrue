import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque
from Funções.ui.musica import buttons

from Funções.global_vars import songs_queues, now_music

async def play(self, interaction:discord.Interaction, musica:str, loop:bool):
    await interaction.response.defer()
    voice_channel = interaction.user.voice.channel

    if voice_channel == None:
        await interaction.followup.send(f"{interaction.user.mention} tem que tar numa chat de voz pra funcionar ;-;")
        return
    
    voice_client = interaction.guild.voice_client

    if voice_client == None:
        voice_client = await discord.VoiceChannel.connect(voice_channel)

    elif voice_channel != voice_client.channel:
        await discord.VoiceChannel.move_to(voice_channel)

    ydl_options = {
        "format": "bestaudio[abr<=96]/bestaudio",
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_his_manifest": False,
    }


    query = "ytsearch1: " + musica
    results = await search_ytdlp_async(query, ydl_options)
    tracks = results.get("entries", [])

    if tracks is None:
        await interaction.followup.send("Sem resultados.")
        return
    
    first_track = tracks[0]
    audio_url = first_track["url"]
    title = first_track.get("title", "Untitled")
    guild_id = str(interaction.guild_id)

    if songs_queues.get(guild_id) is None:
        songs_queues[guild_id] = deque()

    songs_queues[guild_id].append((audio_url, title, loop))

    if now_music.get(guild_id) is None:
        now_music[guild_id] = 0

    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"adicionado na fila: **{title}**")
    else:  
        view = buttons.create_button()

        await interaction.followup.send(f"Tocando agora: **{title}**",view=view)


        await play_next_song(self.bot, voice_client, guild_id, interaction.channel)

async def play_next_song(bot, voice_client, guild_id, channel):
    if songs_queues[guild_id][now_music[guild_id]]:
        audio_url, title, loop = songs_queues[guild_id][now_music[guild_id]]
        if not loop:
            now_music[guild_id] += 1 

        ffmpeg_options = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn -c:a libopus -b:a 96k",
        }
        source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options, executable="bin\\ffmpeg\\ffmpeg.exe")
        def after_play(error):
            if error:
                print(f"Error playing {title}: {error}")

            asyncio.run_coroutine_threadsafe(play_next_song(bot, voice_client, guild_id, channel), bot.loop)

        voice_client.play(source, after=after_play)

        if not loop:
            asyncio.create_task(channel.send(f"Tocando agora: **{title}**"))

    else:

        #await voice_client.disconnect()
        songs_queues[guild_id] = deque()

async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))

def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)