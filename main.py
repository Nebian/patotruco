import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from discord import FFmpegPCMAudio
import random
from random import choice
from typing import Literal
import json
import matplotlib.pyplot as plt
import os
from gtts import gTTS
import asyncio

with open("config.json") as file:
    cfg = json.load(file)

bot = commands.Bot(command_prefix='$', owner_id=295498594604154890, intents=discord.Intents.all())

status = ['Hackeando PATOTRUCO']

@bot.event
async def on_ready():
    change_status.start()
    print("Captain Teemo on duty! {0.user}".format(bot))

@bot.command()
async def resync(ctx):
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Game(choice(status)))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if random.randint(1, 100) == 69:
        await message.channel.send("Tu argumento no tiene sentido.", reference=message, mention_author=False)
    elif random.randint(1, 1000) == 69:
        with open("Media/ascii/train.txt", "r") as renfe:
            rodalies = renfe.read()
        await message.channel.send(rodalies)
    elif random.randint(1, 200) == 69:
        await message.channel.send("Doxing user...", reference=message, mention_author=False)

    await bot.process_commands(message)


def get_salute_audio(user):
    audio_path = os.path.join("", "Media")
    audio_path = os.path.join(audio_path, "audio")
    text = f"Hola {user}, te estoy vigilando."
    tts = gTTS(text, lang="es")
    audio_file = os.path.join(audio_path, f"saludo.mp3")
    tts.save(audio_file)
    return audio_file

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:  # user joined a voice channel
        channel = after.channel
        voice_client = await channel.connect()
        audio_file = get_salute_audio(member.name)
        audio_source = FFmpegPCMAudio(audio_file, executable="ffmpeg")
        voice_client.play(audio_source)
        while voice_client.is_playing():
            await asyncio.sleep(0.1)
        await asyncio.sleep(1)
        await voice_client.disconnect(force=True)


@bot.tree.command(name="ping", description="Imprime el ping entre el bot y el servidor")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"**Pong!** Latency {round(bot.latency * 1000)}ms", ephemeral=True)


@bot.tree.command(name="sleepy", description="Envía un giff de Tom con sueño")
async def sleepy(interaction: discord.Interaction):
    await interaction.response.send_message(file=discord.File('Media/sleepy-sleeping.gif'))


@bot.tree.command(name="pepe", description="Envía un video que explica el origen de Pepe la rana")
async def pepe(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.youtube.com/watch?v=mxpbwpU9HAo&ab_channel=theScoreesports")


@bot.tree.command(name="rolldice", description="Tira un dado")
@app_commands.describe(dices="Dados disponibles")
async def rolldice(interaction: discord.Interaction, dices: Literal['4', '6', '8', '10', '12', '20']):
    await interaction.response.send_message(f"Es un **{random.randint(1, int(dices))}**!")


bot.run(cfg['token'])
