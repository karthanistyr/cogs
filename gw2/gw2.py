import discord
import datetime
import re
from enum import Enum
from .utils.dataIO import dataIO
from discord.ext import commands
from gw2api.model.Query import Querier

#from https://wiki.guildwars2.com/wiki/Template:Rarity
class gw2_constants:
    def __init__(self):
        self.rarity_colour = {
                "Junk": 0xAAAAAA,
                "Fine": 0x62A4DA,
                "Masterwork": 0x1a9306,
                "Rare": 0xfcd00b,
                "Exotic": 0xffa405,
                "Ascended": 0xfb3e8d,
                "Legendary": 0x4C139D,
                "Basic": 0xFFFFFF }

class gw2:
    def __init__(self, bot):
        self.bot = bot
        self.locales = dataIO.load_json("data/gw2/localised_strings.json")

        #default (hardcode) to french locale for now
        self.locale = "fr"
        #shortcut to localised strings
        self.strings = self.locales[self.locale]

    def loadApiKeys(self):
        keys = {}
        filename = "data/gw2/api_keys.json"
        if(dataIO.is_valid_json(filename)):
            keys = dataIO.load_json(filename)
        return keys

    def writeKeys(self, keys):
        dataIO.save_json("data/gw2/api_keys.json", keys)

    def loadGuildKeys(self):
        keys = {}
        filename = "data/gw2/guild_keys.json"
        if(dataIO.is_valid_json(filename)):
            keys = dataIO.load_json(filename)
        return keys

    def write_guild_keys(self, keys):
        dataIO.save_json("data/gw2/guild_keys.json", keys)

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

        api_client = Querier()
        chars = api_client.get_characters(apiKey)

        em = discord.Embed(title=self.strings["characters_title"].format(ctx.message.author.name))
        for char in chars:
            em.add_field(name="Personnage", value=char, inline=True)

        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def character(self, ctx, char_name):
        apiKey = self.getUserKey(ctx.message.author.id)
        if(apiKey is None):
            await self.bot.say(self.strings["no_key_exists"])
            return

        api_client = Querier()
        char = api_client.get_character(char_name, self.locale, apiKey)

        if(not char.has_loaded):
            await self.bot.say("Personnage introuvable.")
            return

        em = discord.Embed(title="_{}_".format(char.object.title.object.name if (char.object.title is not None and char.object.title.has_loaded) else self.strings["titleless"]))
        em.set_author(name=char.object.name)
        em.add_field(name=self.strings["profession"], value=char.object.profession, inline=True)
        em.add_field(name=self.strings["level"], value=char.object.level, inline=True)
        em.add_field(name=self.strings["race"], value=char.object.race, inline=True)
        em.add_field(name=self.strings["death"], value="{} {}".format(char.object.deaths, self.strings["times"]), inline=True)
        em.add_field(name=self.strings["age"], value="{}".format(str(datetime.timedelta(seconds=char.object.age))), inline=True)

        await self.bot.say(embed=em)

    def validate_api_key_format(self, api_key):
    # example format:
    # 12345678-ABCD-1234-ABCD-0123456789ABCDEF0123-1234-ABCD-1234-1A2B3C4D5E6F
        pattern =  "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}"
        pattern += "-[a-fA-F0-9]{4}-[a-fA-F0-9]{20}-[a-fA-F0-9]{4}"
        pattern += "-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        match = re.match(pattern, api_key)
        return match is not None

    def validate_string_input(self, str, min_length=3, max_length=20, allowed_chars="[a-zA-Z0-9]"):
        rgxp_pattern = "^{}{{{},{}}}$".format(allowed_chars, min_length, max_length)
        match = re.match(rgxp_pattern, str)
        return match is not None

    @commands.command()
    async def storeguildkey(self, guild_acronym, api_key=None):
        if(api_key is None):
            await self.bot.say(self.strings["no_key_passed"])
            return

        if(not self.validate_api_key_format(api_key)):
            await self.bot.say(self.strings["wrong_key_format"])
            return

        if(not self.validate_string_input(guild_acronym)):
            await self.bot.say(self.strings["wrong_guild_alias_format"])
            return

        keys = self.loadGuildKeys()

        if(guild_acronym in keys):
            await self.bot.say(self.strings["key_exists_warning"])
        else:
            keys[guild_acronym] = api_key

        self.write_guild_keys(keys)
        await self.bot.say(self.strings["command_completed"])

    @commands.command()
    async def deleteguildkey(self, guild_acronym):
        if(not validate_string_input(guild_acronym)):
            await self.bot.say(self.strings["wrong_guild_alias_format"])
            return

        keys = self.loadGuildKeys()

        if(guild_acronym in keys):
            del keys[guild_acronym]

        self.write_guild_keys(keys)
        await self.bot.say(self.strings["command_completed"])

    @commands.command(pass_context=True)
    async def storekey(self, ctx, api_key=None):
        if(api_key is None):
            await self.bot.say(self.strings["no_key_passed"])
            return

        if(not self.validate_api_key_format(api_key)):
            await self.bot.say(self.strings["wrong_key_format"])
            return

        keys = self.loadApiKeys()

        if(ctx.message.author.id in keys):
            await self.bot.say(self.strings["key_exists_warning"])
        else:
            keys[ctx.message.author.id] = api_key

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
