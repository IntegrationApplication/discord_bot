# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.message_content = True
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

# @client.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')


@bot.command()
async def plouf(ctx):
    await ctx.send("I'm happy")


@bot.command()
async def plouf2(ctx, args):
    await ctx.send(f"I'm happy 2: {args}")

# client.run(TOKEN)
bot.run(TOKEN)
