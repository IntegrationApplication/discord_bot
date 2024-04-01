# bot.py
import os

import discord
from discord import app_commands
from discord.ext import commands
# from dotenv import load_env
import secret
import character_api
import requests
import io

# load_env()
# TOKEN = os.getenv("DISCORD_TOKEN")
TOKEN = secret.DISCORD_TOKEN

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


###############################################################################
#                                   on ready                                  #
###############################################################################

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user.name} has connected to Discord!')


###############################################################################
#                                   sync tree                                 #
###############################################################################

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

###############################################################################
#                               commande basique                              #
###############################################################################


@bot.tree.command(name="plouf")
async def plouf(interaction: discord.Interaction):
    await interaction.response.send_message("I'm happy")

# @bot.command(name="plouf")
# async def plouf(ctx):
#     await ctx.send("I'm happy")

###############################################################################
#                                avec argument                                #
###############################################################################


@bot.tree.command(name="upper")
@app_commands.describe(arg="string to upper")
async def upper(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"upper string {arg.upper()}!")


###############################################################################
#                        test requesting dnd database                         #
###############################################################################

@bot.tree.command(name="sdnd")
@app_commands.describe(search="something to search")
async def sdnd(interaction: discord.Interaction, search: str):
    url = "https://www.dnd5eapi.co/api/" + "".join(search.split(' '))
    resp = requests.get(url)
    if resp.status_code == 200:
        await interaction.response.send_message(resp.text)
    else:
        await interaction.response.send_message("request error")


###############################################################################
#                    test getting user id from interaction                    #
###############################################################################

@bot.tree.command(name="id")
async def id(interaction: discord.Interaction):
    await interaction.response.send_message(f"Id: {interaction.user.id}")


###############################################################################
#                        test creating a text channel                         #
###############################################################################

@bot.tree.command(name="testcreatechannel",
                  description="create a text channel")
@app_commands.describe(name="name of the channel")
async def testcreatechannel(interaction: discord.Interaction, name: str):
    guild = interaction.guild
    channel = await guild.create_text_channel(name)
    if channel is None:
        await interaction.response.send_message(f"channel {name} not created")
    else:
        await interaction.response.send_message(f"channel {name} created")


###############################################################################
#                  post image from keywords in a channel                      #
###############################################################################

@bot.tree.command(name="genimage",
                  description="generate an image from keywords")
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


###############################################################################
#                                    roll                                     #
###############################################################################

@bot.tree.command(name="roll", description="roll a stat")
async def roll_any(interaction: discord.Interaction, stat: str):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    url = character_api.rollAnyURL(user_id, channel_id, stat)
    print(url)

    resp = requests.get(url)
    await interaction.response.send_message(resp.text)


@bot.tree.command(name="attack", description="attack attack with a weapon")
async def roll_attack(interaction: discord.Interaction, weaponidx: int):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    url = character_api.rollAttackURL(user_id, channel_id, weaponidx)
    print(url)

    resp = requests.get(url)
    await interaction.response.send_message(resp.text)


@bot.tree.command(name="damage", description="roll damage with a weapon")
async def roll_damage(interaction: discord.Interaction, weaponidx: int):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    url = character_api.rollDamageURL(user_id, channel_id, weaponidx)
    print(url)

    resp = requests.get(url)
    await interaction.response.send_message(resp.text)


@bot.tree.command(name="init", description="roll initiative")
async def roll_initiative(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    url = character_api.rollInitiativeURL(user_id, channel_id)
    print(url)

    resp = requests.get(url)
    await interaction.response.send_message(resp.text)


###############################################################################
#                       create and modify a character                         #
###############################################################################

@bot.tree.command(name="modif", description="modify character")
async def modify_character(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    outputUrl = character_api.modifyCharacterURL(user_id, channel_id)
    print(outputUrl)

    await interaction.response.send_message(outputUrl)


@bot.tree.command(name="create", description="create character")
async def create_character(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = interaction.channel_id

    # create the character
    createUrl = character_api.createCharacterURL(user_id, channel_id)
    print(createUrl)
    resp = requests.post(createUrl)
    print(resp.text)
    print(resp.status_code)

    if resp.status_code == 200:
        # output the modify url
        outputUrl = character_api.modifyCharacterURL(user_id, channel_id)
        await interaction.response.send_message(outputUrl)
    else:
        await interaction.response.send_message(resp.text)


@bot.tree.command(name="delete", description="delete character")
async def delete_character(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    deleteUrl = character_api.deleteCharacterURL(user_id, channel_id)
    print(deleteUrl)
    resp = requests.delete(deleteUrl)
    print(resp.text)

    await interaction.response.send_message("character deleted")


@bot.tree.command(name="bleed", description="take damage")
@app_commands.describe(amount="amount of damage taken")
async def bleed(interaction: discord.Interaction, amount: int):
    user_id = interaction.user.id
    channel_id = interaction.channel_id

    # create the character
    url = character_api.takeDamageURL(user_id, channel_id, amount)
    resp = requests.put(url)
    if resp.status_code == 200:
        await interaction.response.send_message(
                f"{amount} damage taken (current Hp: {resp.text})")
    else:
        await interaction.response.send_message(resp.text)


###############################################################################
#                                list commands                                #
###############################################################################

@bot.tree.command(name="stats", description="list stats")
async def list_stats(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    url = character_api.listStatsURL(user_id, channel_id)
    resp = requests.get(url)

    await interaction.response.send_message(resp.text)


@bot.tree.command(name="skills", description="list skills")
async def list_skills(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    url = character_api.listSkillsURL(user_id, channel_id)
    resp = requests.get(url)

    await interaction.response.send_message(resp.text)


@bot.tree.command(name="savings", description="list saving throws")
async def list_savings(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    url = character_api.listSavingsThrowsURL(user_id, channel_id)
    resp = requests.get(url)

    await interaction.response.send_message(resp.text)


@bot.tree.command(name="weapons", description="list weapons")
async def list_weapons(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    url = character_api.listWeaponsURL(user_id, channel_id)
    resp = requests.get(url)

    await interaction.response.send_message(resp.text)


@bot.tree.command(name="infos",
                  description="list informations on the character")
async def list_infos(interaction: discord.Interaction):
    user_id = interaction.user.id
    channel_id = interaction.channel_id
    url = character_api.listInfosURL(user_id, channel_id)
    resp = requests.get(url)

    await interaction.response.send_message(resp.text)

###############################################################################
#                               lauch the bot                                 #
###############################################################################

bot.run(TOKEN)
