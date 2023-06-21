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
            
            for channel in context.guild.text_channels:
                counter = await __deletechannel_func(target, channel, counter)
            
            for thread in context.guild.threads:
                counter = await __deletechannel_func(target, thread, counter)
            
            #for forum in context.guild.forums:
            #    for thread in forum.threads:
            #        counter = await __deletechannel_func(target, thread, counter)
                        
            string_to_send = confirm_string + target_name + "! " + str(counter) + end_string
            await context.send(string_to_send)

    @bot.command(name='deletechall')
    @has_permissions(manage_messages=True)
    async def deletechall_func(context, target: discord.User, channel):
        if context.author.guild_permissions.manage_messages:
            
            counter = 0
            target_name = '<@' + str(target.id) + '>'
            
            channel, valid = intTryParse(channel)
            if valid:
                channel = await context.guild.fetch_channel(channel)
                if(channel is not None):
                    counter = await __deletechannel_func(target, channel, counter)
                        
            string_to_send = confirm_string + target_name + "! " + str(counter) + end_string
            await context.send(string_to_send)

    async def __deletechannel_func(target, channel, counter):
        print("Testing " + channel.name + ", type:" + str(channel.type))

        if str(channel.type) == 'text' or str(channel.type).endswith('thread'):
            
            old_state = None
            if str(channel.type).endswith('thread'):
                old_state = channel.archived
                await channel.edit(archived = False)
            last_msg = None
            iterations = 1
            done = False
            try:
                while not done:
                    try:
                        messages = [message async for message in channel.history(limit = TOTAL_MSG_TESTED, after=last_msg, oldest_first=True)]
                        print("Iteration: " + str(iterations))
                        iterations += 1
                        
                        if (messages is not None) and (len(messages) != 0):
                            for message in messages:
                                if message.author == target:
                                    counter += 1
                                    while True:
                                        try:
                                            await message.delete()
                                            break
                                        except discord.errors.HTTPException as e:
                                            print(e)
                                            if(str(e).startswith("403")):
                                                break
                            if len(messages) < TOTAL_MSG_TESTED:
                                done = True
                            else:
                                last_msg = messages[TOTAL_MSG_TESTED - 1]
                        else:
                            done = True
                    except discord.errors.DiscordServerError:
                        print("Received a reset, sleeping for 5 minutes!")
                        await asyncio.sleep(5 * 60)
                    except ClientOSError:
                        print("Received a reset, sleeping for 5 minutes!")
                        await asyncio.sleep(5 * 60)
                    
            except discord.Forbidden:
                print("Kicked from " + channel.name + "!")
                
            if str(channel.type).endswith('thread'):
                await channel.edit(archived = old_state)

        return counter
    