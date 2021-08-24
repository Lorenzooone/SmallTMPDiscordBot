import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from timedCollection import *
from aiohttp import ClientOSError

confirm_string = "Cancellati i messaggi di "
end_string = " messaggi cancellati!"
TOTAL_MSG_TESTED = 10000

def setBotData(bot):

    @bot.command(name='deleteall')
    @has_permissions(manage_messages=True)
    async def deleteall_func(context, target: discord.User):
        if context.author.guild_permissions.manage_messages:
            
            counter = 0
            target_name = '<@' + str(target.id) + '>'
            
            for channel in context.guild.channels:
                print("Testing " + channel.name + ", type:" + str(channel.type))
                
                if str(channel.type) == 'text':
                    
                    last_msg = None
                    iterations = 1
                    done = False
                    try:
                        while not done:
                            try:
                                messages = await channel.history(limit = TOTAL_MSG_TESTED, after=last_msg, oldest_first=True).flatten()
                                print("Iteration: " + str(iterations))
                                iterations += 1
                                
                                if (messages is not None) and (len(messages) != 0):
                                    for message in messages:
                                        if message.author == target:
                                            counter += 1
                                            await message.delete()
                                    if len(messages) < TOTAL_MSG_TESTED:
                                        done = True
                                    else:
                                        last_msg = messages[TOTAL_MSG_TESTED - 1]
                                else:
                                    done = True
                            except ClientOSError:
                                print("Received a reset, sleeping for 5 minutes!")
                                await asyncio.sleep(5 * 60)
                                
                            
                    except discord.Forbidden:
                        print("Kicked from " + channel.name + "!")
                        
            string_to_send = confirm_string + target_name + "! " + str(counter) + end_string
            await context.send(string_to_send)
    