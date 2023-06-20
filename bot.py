# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from timedCollection import *

TIME_VALUE = 2

load_dotenv()

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

from timeout import setBotData
timeouts = setBotData(bot)
from deleteall import setBotData
setBotData(bot)

@bot.event
async def on_ready():
    global timeouts
    await timeouts.readData()
    while True:
        await asyncio.sleep(TIME_VALUE)
        await timeouts.check_times()

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
