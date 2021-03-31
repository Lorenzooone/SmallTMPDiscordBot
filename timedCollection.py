from dateutil.parser import parse
import datetime
from threading import Timer
import os
import asyncio

time_types = {"s": 1, "m": 1*60, "h": 1*60*60, "d": 1*60*60*24,\
              "w": 1*60*60*24*7}

time_strings = {"s": ("secondo", "secondi"), "m": ("minuto", "minuti"), "h": ("ora", "ore"),\
                "d": ("giorno", "giorni"), "w": ("settimana", "settimane")}

def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

# Class that implements the timed Collection, which after a set amount of time checks
# if someone has to be removed from the list
class timedCollection:
    def __init__(self, path, bot, action):
        self.collection = dict()
        self.path = path
        self.action = action
        self.bot = bot
    
    async def readData(self):
        if os.path.isfile(self.path):
            with open(self.path, 'r', encoding='utf-8') as ifile:
                lines = ifile.readlines()
            
            # Get old data, if there even is
            for i in range(0 ,len(lines), 3):
                if(lines[i] is not None and lines[i] != ""):
                    if(lines[i + 1] is not None and lines[i + 1] != ""):
                        if(lines[i + 2] is not None and lines[i + 2] != ""):
                        
                            # Handle "TIMED ACTION" removals after a shutdown
                            datet = parse(lines[i + 2])
                            user_id = intTryParse(lines[i])
                            guild_id = intTryParse(lines[i + 1])
                            
                            if (guild_id[1]):
                                guild = self.bot.get_guild(guild_id[0])
                                if (guild is not None) and (user_id[1]):
                                    member = await guild.fetch_member(user_id[0])
                                
                                    if member is not None:
                                        # Put this in the collection
                                        self.collection[member] = datet
    
    async def check_times(self):
        tmp_collection = dict()
        for key in self.collection.keys():
            tmp_collection[key] = self.collection[key]
        for key in tmp_collection.keys():
            if tmp_collection[key] <= datetime.datetime.now():
                await self.remove_entry(key)

    def update_file(self):
        with open(self.path, 'w', encoding='utf-8') as ofile:
            for key in self.collection.keys():
                ofile.write(str(key.id) + '\n')
                ofile.write(str(key.guild.id) + '\n')
                ofile.write(str(self.collection[key]) + '\n')
    
    def has_entry(self, user):
        return user in self.collection.keys()

    async def remove_entry(self, user):
        await self.action(user)
        if user in self.collection.keys():
            self.collection.pop(user)
            self.update_file()

    async def add_entry(self, user, value, value_type):
        
        # Handle <= 0 as an input value
        if value <= 0:
            await self.remove_entry(user)
        else:
            self.collection[user] = datetime.datetime.now() + datetime.timedelta(seconds=time_types[value_type]*value)
            self.update_file()
