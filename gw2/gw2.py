import discord
import requests
from .utils.dataIO import fileIO
from discord.ext import commands

class gw2_api_client:
    def __init__(self):
        self.root_api_endpoint = "https://api.guildwars2.com"

    def get_request(self, endpoint, arguments, api_key=None):
        complete_endpoint = self.root_api_endpoint + endpoint

        if(api_key is not None):
            headers = {"Authorization": "Bearer {}".format(api_key)}

        get_response = requests.get(complete_endpoint, params=arguments, headers=headers)

        if(get_response.status_code == 200):
            return get_response.json()

    def get_characters(self, api_key):
        ep = "/v2/characters"

        char_data = self.get_request(ep, None, api_key)
        return char_data

class gw2:
    def __init__(self, bot):
        self.bot = bot
        self.strings = fileIO("data/gw2/localised_strings.json", "load")

        #default (hardcode) to french locale for now
        self.locale = "fr"
        self.strngs = self.strings[self.locale]

    def loadApiKeys(self):
        keys = fileIO("data/gw2/api_keys.json", "load")
        return keys

    def writeKeys(self, keys):
        fileIO("data/gw2/api_keys.json", "save", keys)

    def getUserKey(self, userId):
        keys = self.loadApiKeys()
        if(userId in keys):
            return keys[userId]

    @commands.command(pass_context=True)
    async def characters(self, ctx):
        apiKey = self.getUserKey(ctx.message.author.id)
        if(apiKey is None):
            await self.bot.say(self.strings[self.locale]["no_key_exists"])
            return

        api_client = gw2_api_client()

        chars = api_client.get_characters(apiKey)

        em = discord.Embed(title=self.strngs["characters_title"].format(ctx.message.author.mention))
        for char in chars:
            em.add_field(name="char", value=char, inline=True)

        #response = self.bot.loop.run_in_executor(None, em)
        #result = await asyncio.wait_for(response, timeout=10)
        await self.bot.say(embed=em)

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
