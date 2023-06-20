import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from timedCollection import *

punishment_string = " non potrà scrivere per "
pardon_string = "Rimosso il timeout da "

def setBotData(bot):

    ROLE = os.getenv('TIMEOUT_ROLE')
    PATH = os.getenv('TIMEOUT_PATH')

    async def remove_timeout(target):
        timeout_role = discord.utils.get(target.guild.roles, name=ROLE)
        await target.remove_roles(timeout_role)
        
    timeouts = timedCollection(PATH, bot, remove_timeout)
        
    @bot.command(name='t')
    async def t_func(context, target: discord.User, num=10, numtype="s"):
        await timeout_func(context, target, num, numtype)
            
    @bot.command(name='timeout')
    @has_permissions(manage_roles=True)
    async def timeout_func(context, target: discord.User, num=10, numtype="s"):
        if context.author.guild_permissions.manage_roles:
            if not target.guild_permissions.manage_roles:
                num, valid = intTryParse(num)
                if valid:
                    if numtype in time_types.keys():
                        
                        target_name = '<@' + str(target.id) + '>'
                        if num > 0:
                            timeout_role = discord.utils.get(target.guild.roles,name=ROLE)
                            await target.add_roles(timeout_role)
                            string_to_send = target_name + punishment_string + str(num) + " "
                            if num == 1:
                                string_to_send += time_strings[numtype][0]
                            else:
                                string_to_send += time_strings[numtype][1] 
                            await context.send(string_to_send + ".")
                        else:
                            if timeouts.has_entry(target):
                                await context.send(pardon_string + target_name + ".")
                        await timeouts.add_entry(target, num, numtype)

    @timeout_func.error
    async def timeout_func_error(error, ctx):
        if isinstance(error, CheckFailure):
            pass
    
    return timeouts
    
