import discord
import requests
from .utils.dataIO import fileIO
from discord.ext import commands

class gw2:
    def __init__(self, bot):
        self.bot = bot
        self.strings = fileIO("data/gw2/localised_strings.json", "load")
        
        #default (hardcode) to french locale for now
        self.locale = "fr"

    def loadApiKeys(self):
        keys = fileIO("data/gw2/api_keys.json", "load")
        return keys

    def writeKeys(self, keys):
        fileIO("data/gw2/api_keys.json", "save", keys)

    @commands.command(pass_context=True)
    async def characters(self, ctx):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff to " + ctx.message.author.mention  + "!")

    @commands.command(pass_context=True)
    async def storekey(self, ctx, apiKey=None):
        if(apiKey is None):
            await self.bot.say(self.strings[self.locale]["no_key_passed"])
            return
        
        keys = self.loadApiKeys()

        if(ctx.message.author.id in keys):
            await self.bot.say(self.strings[self.locale]["key_override_warning"])
        else:
            keys[ctx.message.author.id] = apiKey

        self.writeKeys(keys)
    
    @commands.command(pass_context=True)
    async def deletekey(self, ctx):
    
        keys = self.loadApiKeys()

        if(ctx.message.author.id in keys):
            del keys[ctx.message.author.id]
        
        self.writeKeys(keys)

def setup(bot):
    bot.add_cog(gw2(bot))
