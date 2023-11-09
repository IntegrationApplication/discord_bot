# bot.py
import os

import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from random import randint
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

################################################################################
#                                   on ready                                   #
################################################################################

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"command synced: {synced}")
    except Exception as e:
        print(e)

################################################################################
#                               commande basique                               #
################################################################################

@bot.tree.command(name="plouf")
async def plouf(interaction: discord.Interaction):
    await interaction.response.send_message("I'm happy")

# @bot.command(name="plouf")
# async def plouf(ctx):
#     await ctx.send("I'm happy")

################################################################################
#                                avec argument                                 #
################################################################################

@bot.tree.command(name="upper")
@app_commands.describe(arg="string to upper")
async def upper(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"upper string {arg.upper()}!")

################################################################################
#                                     test                                     #
################################################################################

def _roll(nb_dices: int, faces: int):
    res = 0
    for _ in range(nb_dices):
        res += randint(1, faces)
    return res

@bot.tree.command(name="roll")
@app_commands.describe(dice="1d20")
async def roll(interaction: discord.Interaction, dice: str):
    infos = dice.split('d')
    if len(infos) != 2:
        await interaction.response.send_message("invalid dice")
    else:
        nb_dices = int(infos[0])
        faces = int(infos[1])
        result = _roll(nb_dices, faces)
        await interaction.response.send_message(f"result for {nb_dices}d{faces}: {result}")


################################################################################
#                         test requesting dnd database                         #
################################################################################

@bot.tree.command(name="sdnd")
@app_commands.describe(search="something to search")
async def sdnd(interaction: discord.Interaction, search: str):
    url = "https://www.dnd5eapi.co/api/" + "".join(search.split(' '))
    resp = requests.get(url)
    if resp.status_code == 200:
        await interaction.response.send_message(resp.text)
    else:
        await interaction.response.send_message("request error")



bot.run(TOKEN)
