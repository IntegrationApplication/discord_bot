# bot.py
import os

import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from random import randint
import requests
import io

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
    print(f'{bot.user.name} has connected to Discord!')


################################################################################
#                                   sync tree                                  #
################################################################################

@bot.command()
async def syncglobal(ctx):
    print("syncing globally")
    synced = await ctx.bot.tree.sync()
    print(f"command synced: {synced}")


@bot.command()
async def synclocal(ctx):
    print(f"syncing on  {ctx.guild}")
    synced = await ctx.bot.tree.sync(guild=ctx.guild)
    print(f"command synced: {synced}")

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

@bot.tree.command(name="testcreatechannel", description="create a text channel")
@app_commands.describe(name="name of the channel")
async def testcreatechannel(interaction: discord.Interaction, name: str):
    guild = interaction.guild
    channel = await guild.create_text_channel(name)
    if channel is None:
        await interaction.response.send_message(f"channel {name} not created")
    else:
        await interaction.response.send_message(f"channel {name} created")


################################################################################
#                   post image from keywords in a channel                      #
################################################################################

@bot.tree.command(name="genimage", description="generate an image from keywords")
@app_commands.describe(prompt="prompt to generate the image")
async def genimage(interaction: discord.Interaction, prompt: str):
    url = "https://api-inference.huggingface.co/models/openskyml/dalle-3-xl"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f'Bearer {os.getenv("HUGGINGFACE_API_KEY")}'
    }
    payload = {
        "inputs": prompt,
    }
    response = requests.post(url, headers=headers, json=payload)
    file = discord.File(io.BytesIO(response.content), filename="image.jpeg")
    await interaction.response.send_message(file=file)


@bot.tree.command(name="wololo", description="wololo")
async def wololo(interaction: discord.Interaction):
    await interaction.response.send_message("Wololooooo !")


bot.run(TOKEN)
