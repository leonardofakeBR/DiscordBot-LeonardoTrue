import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

def search_embed(user_avatar, user_name, title, thumbnail, duration):
    seconds = duration % 60
    minutes = duration // 60

    embed=discord.Embed(title=f"{title}", color=0x040829)

    embed.set_thumbnail(url=f"{thumbnail}")

    embed.add_field(name="Duração:",value=f"{minutes}:{seconds}")

    embed.timestamp = datetime.now(timezone.utc)

    embed.set_footer(text=f"{user_name}", icon_url=user_avatar)
    
    return embed