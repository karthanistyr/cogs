import discord
import requests
import urllib
import datetime
from enum import Enum
#from .utils.dataIO import fileIO
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

    def get_characters(self, api_key, char_name=None):
        ep = "/v2/characters"

        safe_char_name = ""
        if(char_name is not None):
            safe_char_name = urllib.parse.quote(char_name)

        char_data = self.get_request(ep + "/" + safe_char_name, None, api_key)
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

    def get_items(self, ids, lang=None):
        ep_items = "/v2/items"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        items = self.get_request(ep_items, args)
        return items

    def get_titles(self, ids, lang=None):
        ep_titles = "/v2/titles"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        titles = self.get_request(ep_titles, args)
        return titles

class gw2_high_level_api_client:

    class title:
        def __init__(self, json=None):
            self.id = None
            self.name = None

            if(json is not None):
                self.load_from_json(json)

        def load_from_json(self, json):
            self.id = json.get("id", None)
            self.name = json.get("name", None)

        def __str__(self):
            return "{}".format(self.name)

    class item_details:
        def __init__(self, json=None):
            self.type = None
            self.damage_type = None
            self.weight_class = None
            self.min_power = None
            self.max_power = None
            self.defense = None
            self.infusion_slots = []
            self.infix_upgrade = None # TODO: infix_upgrade type
            self.suffix_item_id = None # type item
            self.secondary_suffix_item_id = None # type item

            if(json is not None):
                self.load_from_json(json)

        def load_from_json(self, json):
            self.type = json.get("type", None)
            self.damage_type = json.get("damage_type", None)
            self.weight_class = json.get("weight_class", None)
            self.min_power = json.get("min_power", None)
            self.max_power = json.get("max_power", None)
            self.defense = json.get("defense", None)
            self.infusion_slots = [] # TODO
            self.infix_upgrade = None # TODO: infix_upgrade type
            self.suffix_item_id = None # type item # TODO
            self.secondary_suffix_item_id = None # type item # TODO

    class item:
        def __init__(self, json=None):
            self.name = None
            self.description = None
            self.type = None
            self.level = None
            self.rarity = None
            self.vendor_value = None
            self.default_skin = None
            self.game_types = []
            self.flags = []
            self.restrictions = []
            self.id = None
            self.chat_link = None
            self.icon = None
            self.details = None # type: item_details

            if(json is not None):
                self.load_from_json(json)

        def load_from_json(self, json):
            self.name = json.get("name", None)
            self.description = json.get("description", None)
            self.type = json.get("type", None)
            self.level = json.get("level", None)
            self.rarity = json.get("rarity", None)
            self.vendor_value = json.get("vendor_value", None)
            self.default_skin = json.get("default_skin", None)
            self.game_types = json.get("game_types", None)
            self.flags = json.get("flags", None)
            self.restrictions = json.get("restrictions", None)
            self.id = json.get("id", None)
            self.chat_link = json.get("chat_link", None)
            self.icon = json.get("icon", None)
            self.details = gw2_high_level_api_client.item_details(json["details"]) # type: item_details

        def __str__(self):
            return "{}".format(self.name)

    class achievement_reward:
        def __init__(self, json=None):
            self.type = None
            self.id = None
            self.count = None
            self.item = None
            self.title = None

            if(json is not None):
                self.load_from_json(json)

        def load_from_json(self, json):
            self.type = json.get("type", None)
            self.id = json.get("id", None)
            self.count = json.get("count", None)

        def load_item_data(self, item):
            self.item = item

        def load_title_data(self, title):
            self.title = title

        def __str__(self):
            if(self.item is not None):
                return "{} x{}".format(self.item.name, self.count)
            if(self.title is not None):
                return "{}".format(self.title.name)
            else:
                return "{} ({}) x{}".format(self.type, self.id, self.count)

    class achievement_tier:
        def __init__(self, json=None):
            self.count = None
            self.points = None

            if(json is not None):
                self.load_from_json(json)

        def load_from_json(self, json: dict):
            self.count = json.get("count", None)
            self.points = json.get("points", None)

    class achievement:
        def __init__(self, id, json=None):
            self.id = id
            self.name = None
            self.description = None
            self.requirement = None
            self.locked_text = None
            self.type = None
            self.flags = []
            self.tiers = []
            self.rewards = []

            if(json is not None):
                self.load_from_json(json)

        def load_from_json(self, json: dict):
            self.id = json.get("id", None)
            self.name = json.get("name", None)
            self.description = json.get("description", None)
            self.requirement = json.get("requirement", None)
            self.locked_text = json.get("locked_text", None)
            self.type = json.get("type", None)
            self.flags = json.get("flags", None)
            self.tiers = []
            for tier in json["tiers"]:
                self.tiers.append(gw2_high_level_api_client.achievement_tier(tier))
            self.rewards = []
            for rew in json["rewards"]:
                self.rewards.append(gw2_high_level_api_client.achievement_reward(rew))

    class crafting:
        def __init__(self, json=None):
            self.discipline = None
            self.rating = None
            self.active = None

            if(json is not None):
                self.load_from_json(json)

        def load_from_json(self, json: dict):
            self.discipline = json.get("discipline", None)
            self.rating = json.get("rating", None)
            self.active = json.get("active", None)

    class character:
        def __init__(self, json=None):
            self.name = None
            self.race = None
            self.gender = None
            self.flags = []
            self.profession = None
            self.level = None
            self.guild = None
            self.age = None
            self.created = None
            self.deaths = None
            self.crafting = []
            self.title = None
            self.backstory = []
            self.wvw_abilities = []
            self.specializations = []
            self.skills = []
            self.equipement = []
            self.recipes = []
            self.equipment_pvp = []
            self.training = []

            if(json is not None):
                self.load_from_json(json)

        def load_from_json(self, json: dict):
            self.name = json.get("name", None)
            self.race = json.get("race", None)
            self.gender = json.get("gender", None)
            self.flags = []
            self.profession = json.get("profession", None)
            self.level = json.get("level", None)
            self.guild = None # TODO guilde
            self.age = json.get("age", None)
            self.created = json.get("created", None)
            self.deaths = json.get("deaths", None)
            self.crafting = []
            self.title = None # TODO title
            self.backstory = []
            self.wvw_abilities = []
            self.specializations = []
            self.skills = []
            self.equipement = []
            self.recipes = []
            self.equipment_pvp = []
            self.training = []


    def __init__(self):
        self.rest_client = gw2_api_client()

    def get_daily_achievements(self, tomorrow, category, lang=None):
        dailies = self.rest_client.get_dailies(True if (tomorrow == "tomorrow") else False)
        return self.get_achievements(",".join([str(d["id"]) for d in dailies[category]]), lang)

    def get_achievements(self, ids, lang=None):
        achievement_details = self.rest_client.get_daily_quest_details(ids, lang)

        #bulk up item rewards lookups
        items_ids = ",".join([str(qr["id"]) for ach in achievement_details for qr in ach["rewards"] if qr["type"] == "Item"])
        reward_items = self.get_items(items_ids, lang)
        items_data = {}
        for data in reward_items:
            items_data[data.id] = data

        achievement_list = []
        for dailyd in achievement_details:
            ach = gw2_high_level_api_client.achievement(dailyd["id"], dailyd)
            for reward in ach.rewards:
                if(reward.type == "Item"):
                    reward.item = items_data[reward.id]

            achievement_list.append(ach)
        return achievement_list

    def get_items(self, ids, lang=None):
        items_data = self.rest_client.get_items(ids, lang)
        return [gw2_high_level_api_client.item(item_data) for item_data in items_data]

    def get_titles(self, ids, lang=None):
        titles_data = self.rest_client.get_titles(ids, lang)
        return [gw2_high_level_api_client.title(title_data) for title_data in titles_data]

    def get_character(self, key, char_name):
        char_data = self.rest_client.get_characters(key, char_name)
        return gw2_high_level_api_client.character(char_data)

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

        api_client = gw2_api_client()
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

        api_client = gw2_high_level_api_client()
        char = api_client.get_character(apiKey, char_name)

        em = discord.Embed(title=chars.name)

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

        api_client = gw2_high_level_api_client()
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
