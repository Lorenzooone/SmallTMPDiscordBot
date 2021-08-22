import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from timedCollection import *

confirm_string = "Cancellati i messaggi di "
end_string = " messaggi cancellati!"

def setBotData(bot):

    @bot.command(name='deleteall')
    @has_permissions(manage_messages=True)
    async def deleteall_func(context, target: discord.Member, channel: discord.TextChannel):
        if context.author.guild_permissions.manage_messages:
            
            target_name = '<@' + str(target.id) + '>'
            counter = 0
            print("Testing " + channel.name + ", type:" + str(channel.type))
            if str(channel.type) == 'text':
                try:
                    messages = await channel.history(limit = None).flatten()
                    for message in messages:
                        if message.author == target:
                            counter += 1
                            await message.delete()
                except discord.Forbidden:
                    print("Kicked from " + channel.name + "!")
                        
            string_to_send = confirm_string + target_name + "! " + str(counter) + end_string
            await context.send(string_to_send)
    