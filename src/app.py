# bot.py
import os

import discord
from discord import app_commands
from discord.ext import commands
from random import randint
import secret
import character_api
import requests
import io

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

################################################################################
#                                     roll                                     #
################################################################################

@bot.tree.command(name="roll")
@app_commands.describe(dice="roll a stat")
async def roll(interaction: discord.Interaction, stat: str):
    # TODO: get player and channel ids for the requests
    url = character_api.rollAnyURL(1, 1, stat);
    resp = requests.get(url)
    await interaction.response.send_message(resp.text)


@bot.tree.command(name="attack")
@app_commands.describe(dice="attack with a weapon")
async def roll(interaction: discord.Interaction, weaponIndex: int):
    # TODO: get player and channel ids for the requests
    url = character_api.rollAttackURL(1, 1, weaponIndex);
    resp = requests.get(url)
    await interaction.response.send_message(resp.text)


@bot.tree.command(name="damage")
@app_commands.describe(dice="make damage with a weapon")
async def roll(interaction: discord.Interaction, weaponIndex: int):
    # TODO: get player and channel ids for the requests
    url = character_api.rollDamageURL(1, 1, weaponIndex);
    resp = requests.get(url)
    await interaction.response.send_message(resp.text)


@bot.tree.command(name="init")
@app_commands.describe(dice="roll initiative")
async def roll(interaction: discord.Interaction):
    # TODO: get player and channel ids for the requests
    url = character_api.rollInitiativeURL(1, 1);
    resp = requests.get(url)
    await interaction.response.send_message(resp.text)

################################################################################
#                        create and modify a character                         #
################################################################################

@bot.tree.command(name="modif")
@app_commands.describe(dice="roll initiative")
async def roll(interaction: discord.Interaction):
    # TODO: get player and channel ids for the requests
    outputUrl = modifyCharacterURL(1, 1)
    await interaction.response.send_message(outputUrl)


@bot.tree.command(name="create")
@app_commands.describe(dice="roll initiative")
async def roll(interaction: discord.Interaction):
    # TODO: get player and channel ids for the requests

    # create the character
    createUrl = createCharacterURL(1, 1)
    resp = requests.post(createUrl)

    if resp.status_code == 500:
        await interaction.response.send_message(resp.text)
    else:
        # output the modify url
        outputUrl = modifyCharacterURL(1, 1)
        await interaction.response.send_message(outputUrl)

################################################################################
#                                lauch the bot                                 #
################################################################################

bot.run(secret.TOKEN)
