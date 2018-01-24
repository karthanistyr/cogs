import discord
import datetime
from enum import Enum
from .utils.dataIO import fileIO
from discord.ext import commands

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
        self.locales = fileIO("data/gw2/localised_strings.json", "load")

        #default (hardcode) to french locale for now
        self.locale = "fr"
        #shortcut to localised strings
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

        api_client = gw2_api_v2_client()
        chars = api_client.get_characters(apiKey)

        em = discord.Embed(title=self.strings["characters_title"].format(ctx.message.author.name))
        for char in chars:
            em.add_field(name="char", value=char, inline=True)

        await self.bot.say(embed=em)


    @commands.command(pass_context=True)
    async def character(self, ctx, char_name):
        apiKey = self.getUserKey(ctx.message.author.id)
        if(apiKey is None):
            await self.bot.say(self.strings["no_key_exists"])
            return

        api_client = querier()
        char = api_client.get_character(apiKey, char_name, self.locale)

        if(char is None):
            await self.bot.say("Personnage introuvable.")
            return

        #fetch relevant icons
        icons = api_client.get_icons("icon_{},icon_{}_big".format(char.profession.lower(), char.profession.lower()))
        icon_small = icons[0]
        icon_big = icons[1]

        em = discord.Embed(title=char.title.name if char.title is not None else None)
        em.set_author(name=char.name, icon_url=icon_small.icon)
        em.set_thumbnail(url=icon_big.icon)
        em.add_field(name=self.strings["profession"], value=char.profession, inline=True)
        em.add_field(name=self.strings["level"], value=char.level, inline=True)
        em.add_field(name=self.strings["race"], value=char.race, inline=True)
        em.add_field(name=self.strings["death"], value="{} {}".format(char.deaths, self.strings["times"]), inline=True)
        em.add_field(name=self.strings["age"], value="{}".format(str(datetime.timedelta(seconds=char.age))), inline=True)

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

        api_client = querier()
        daily_list = api_client.get_daily_achievements(True if (tomorrow == "tomorrow") else False, category, self.locale)

        em = discord.Embed(title=self.strings["daily_quests_embed_title"].format(category))

        for quest in daily_list:
            rewards_text = ", ".join(["{}".format(str(reward)) for reward in quest.rewards])
            tiers_text = ", ".join(["{} {} (+{} pts)".format(tier.count, self.strings["times"], tier.points) for tier in quest.tiers])
            em.add_field(name=quest.name, value="{}\n{}: {}\n{}: {}\n".format(quest.requirement, self.strings["tiers"], tiers_text, self.strings["rewards"], rewards_text), inline=False)

        await self.bot.say(embed=em)

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
