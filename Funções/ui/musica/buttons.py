import discord
from discord import app_commands
from discord.ext import commands

from Funções.musica import pause
from Funções.musica import resume
from Funções.musica import skip
from Funções.musica import exit
from Funções.musica import loop


def create_button():
    view = discord.ui.View()

    loop_button = discord.ui.Button(label="🔁", style=discord.ButtonStyle.blurple)

    loop_button.callback = loop.loop
    view.add_item(loop_button)

    skip_button = discord.ui.Button(label="⏭", style=discord.ButtonStyle.blurple)

    skip_button.callback = skip.skip
    view.add_item(skip_button)

    pause_button = discord.ui.Button(label="⏸", style=discord.ButtonStyle.blurple)

    pause_button.callback = pause.pause
    view.add_item(pause_button)

    resume_button = discord.ui.Button(label="▶", style=discord.ButtonStyle.blurple)

    resume_button.callback = resume.resume
    view.add_item(resume_button)

    exit_button = discord.ui.Button(label="🏃", style=discord.ButtonStyle.red)

    exit_button.callback = exit.exit
    view.add_item(exit_button)

    return view