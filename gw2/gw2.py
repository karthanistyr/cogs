import discord
import requests
from enum import Enum
from .utils.dataIO import fileIO
from discord.ext import commands

class gw2_api_client:
    def __init__(self):
        self.root_api_endpoint = "https://api.guildwars2.com"

    def get_request(self, endpoint, arguments, api_key=None):
        complete_endpoint = self.root_api_endpoint + endpoint
        headers = None

        if(api_key is not None):
            headers = {"Authorization": "Bearer {}".format(api_key)}

        get_response = requests.get(complete_endpoint, params=arguments, headers=headers)

        if(get_response.status_code == 200):
            return get_response.json()

    def get_characters(self, api_key):
        ep = "/v2/characters"

        char_data = self.get_request(ep, None, api_key)
        return char_data

    def get_dailies(self, tomorrow: bool=None):
        ep_today = "/v2/achievements/daily"
        ep_tomorrow = ep_today + "/tomorrow"

        dailies_data = self.get_request(ep_tomorrow if tomorrow else ep_today, None)
        return dailies_data

    def get_daily_quest_details(self, ids, lang=None):
        ep_daily_details = "/v2/achievements"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        daily_details = self.get_request(ep_daily_details, args)
        return daily_details

class gw2:
    def __init__(self, bot):
        self.bot = bot
        self.locales = fileIO("data/gw2/localised_strings.json", "load")

        #default (hardcode) to french locale for now
        self.locale = "fr"
        self.strings = self.locales[self.locale]

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
            await self.bot.say(self.strings["no_key_exists"])
            return

        api_client = gw2_api_client()

        chars = api_client.get_characters(apiKey)

        em = discord.Embed(title=self.strings["characters_title"].format(ctx.message.author.name))
        for char in chars:
            em.add_field(name="char", value=char, inline=True)

        await self.bot.say(embed=em)

    @commands.command()
    async def dailies(self, category, tomorrow=None):
        if(category is None):
            await self.bot.say(self.strings["missing_parameter"].format("category"))
            return

        valid_categories = {"pve", "pvp", "wvw", "fractals", "special"}
        if(category not in valid_categories):
            await self.bot.say(self.strings["invalid_parameter"].format(category, "category"))
            return

        api_client = gw2_api_client()
        dailies = api_client.get_dailies(True if (tomorrow == "tomorrow") else False)

        daily_ids = []
        for daily in dailies[category]:
            daily_ids.append(str(daily["id"]))

        daily_details = api_client.get_daily_quest_details(",".join(daily_ids), self.locale)

        await self.bot.say(daily_details)

    @commands.command(pass_context=True)
    async def storekey(self, ctx, apiKey=None):
        if(apiKey is None):
            await self.bot.say(self.strings["no_key_passed"])
            return

        keys = self.loadApiKeys()

        if(ctx.message.author.id in keys):
            await self.bot.say(self.strings["key_exists_warning"])
        else:
            keys[ctx.message.author.id] = apiKey

        self.writeKeys(keys)

        await self.bot.say(self.strings["command_completed"])

    @commands.command(pass_context=True)
    async def deletekey(self, ctx):

        keys = self.loadApiKeys()

        if(ctx.message.author.id in keys):
            del keys[ctx.message.author.id]

        self.writeKeys(keys)
        await self.bot.say(self.strings["command_completed"])

def setup(bot):
    bot.add_cog(gw2(bot))
