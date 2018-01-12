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
        strngs = self.strings[self.locale]

    def loadApiKeys(self):
        keys = fileIO("data/gw2/api_keys.json", "load")
        return keys

    def writeKeys(self, keys):
        fileIO("data/gw2/api_keys.json", "save", keys)

    def getUserKey(self, userId):
        keys = self.loadApiKeys()
        if(userId in keys):
            return keys[userId]

    def getRequest(self, endpoint, apiKey):
        rootEndpoint = "https://api.guildwars2.com"
        authorizationHeader = {"Authorization": "Bearer " + apiKey}

        r = requests.get(rootEndpoint + endpoint, headers=authorizationHeader)
        return r.json()

    @commands.command(pass_context=True)
    async def characters(self, ctx):
        apiKey = self.getUserKey(ctx.message.author.id)
        if(apiKey is None):
            await self.bot.say(self.strings[self.locale]["no_key_exists"])
            return

        charData = self.getRequest("/v2/characters", apiKey)

        em = discord.Embed(title=strngs["character_title"].format(ctx.message.author.mention)
        for char in charData:
            em.add_field(*,"char", char, False)
            
        await self.bot.say(em)
        
    @commands.command(pass_context=True)
    async def storekey(self, ctx, apiKey=None):
        if(apiKey is None):
            await self.bot.say(self.strings[self.locale]["no_key_passed"])
            return
        
        keys = self.loadApiKeys()

        if(ctx.message.author.id in keys):
            await self.bot.say(self.strings[self.locale]["key_exists_warning"])
        else:
            keys[ctx.message.author.id] = apiKey

        self.writeKeys(keys)

        await self.bot.say(self.strings[self.locale]["command_completed"])
    
    @commands.command(pass_context=True)
    async def deletekey(self, ctx):
    
        keys = self.loadApiKeys()

        if(ctx.message.author.id in keys):
            del keys[ctx.message.author.id]
        
        self.writeKeys(keys)
        await self.bot.say(self.strings[self.locale]["command_completed"])

def setup(bot):
    bot.add_cog(gw2(bot))
