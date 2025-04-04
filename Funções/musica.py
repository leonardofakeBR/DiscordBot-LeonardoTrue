import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque



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
        await pause(self, interaction)


    @app_commands.command(name="resume", description="Bora continuar ._.")
    async def slash_resume(self, interaction:discord.Interaction):
        await resume(self, interaction)


    @app_commands.command(name="exit", description="Quer privacidade é?")
    async def slash_exit(self, interaction:discord.Interaction):
        await exit(self, interaction)

songs_queues = {}

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

    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"adicionado na fila: **{title}**")
    else:  
        view = discord.ui.View()
        skip_button = discord.ui.Button(label="⏭", style=discord.ButtonStyle.blurple)
        
        skip_button.callback = skip
        view.add_item(skip_button)

        await interaction.followup.send(f"Tocando agora: **{title}**",view=view)
        await play_next_song(self.bot, voice_client, guild_id, interaction.channel)

async def skip(interaction:discord.Interaction):
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        guild_id = str(interaction.guild_id)
        songs_queues[guild_id].popleft()
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("Pulamo essa aberração 0-0")
    else:
        await interaction.response.send_message("Não da pra pular algo que não existe .-.")

async def pause(self, interaction: discord.Interaction):
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

async def resume(self, interaction: discord.Interaction):
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

async def exit(self, interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if not voice_client or not voice_client.is_connected():
        return await interaction.response.send_message("Tá querendo me humilhar é, ja to excluido e quer me tirar ainda ;-;")

    # Clear the guild's queue
    guild_id_str = str(interaction.guild_id)
    if guild_id_str in songs_queues:
        songs_queues[guild_id_str].clear()

    # If something is playing or paused, stop it
    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()

    # (Optional) Disconnect from the channel
    await voice_client.disconnect()

    await interaction.response.send_message("Vo deixar vcs sozinho 0-0")

async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))

def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)

async def play_next_song(bot, voice_client, guild_id, channel):

    if songs_queues[guild_id]:
        audio_url, title, loop = songs_queues[guild_id][0]
        if not loop:
            audio_url, title, loop = songs_queues[guild_id].popleft()
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


async def setup(bot):
    await bot.add_cog(Musica(bot))
