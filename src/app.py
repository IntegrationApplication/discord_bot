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


################################################################################
#                     test getting user id from interaction                    #
################################################################################

@bot.tree.command(name="id")
async def id(interaction: discord.Interaction):
    await interaction.response.send_message(f"your id is {interaction.user.id}")


################################################################################
#                         test creating a text channel                         #
################################################################################

@bot.tree.command(name="createchannel", description="create a text channel")
@app_commands.describe(name="name of the channel")
async def createchannel(interaction: discord.Interaction, name: str):
    guild = interaction.guild
    channel = await guild.create_text_channel(name)
    if channel is None:
        await interaction.response.send_message(f"channel {name} not created")
    else:
        await interaction.response.send_message(f"channel {name} created")


################################################################################
#                 test post image from keywords in a channel                   #
################################################################################

@bot.tree.command(name="postimage", description="post image from url in a channel")
@app_commands.describe(keywords="keywords to search pictures with")
async def postimage(interaction: discord.Interaction, keywords: str):
    url_to_fetch = f'https://api.unsplash.com/photos/random?query={"+".join(keywords.split(" "))}&client_id={os.getenv("UNSPLASH_ACCESS_KEY")}'
    r = requests.get(url_to_fetch)
    image_url = r.json()["urls"]["regular"]
    await interaction.response.send_message(image_url)


bot.run(TOKEN)
