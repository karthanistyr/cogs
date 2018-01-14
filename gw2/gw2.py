import discord
import requests
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

    def get_items(self, ids, lang=None):
        ep_items = "/v2/items"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        items = self.get_request(ep_items, args)
        return items

class gw2_high_level_api_client:

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

            if(json is not None):
                self.load_from_json(json)

        def load_from_json(self, json):
            self.type = json.get("type", None)
            self.id = json.get("id", None)
            self.count = json.get("count", None)

        def load_item_data(self, item):
            self.item = item

        def __str__(self):
            if(self.item is not None):
                return "{} x{}".format(str(self.item), self.count)
            else:
                return "{} ({}) x{}".format(self.type, self.id, self.count)

    class achievement_tier:
        def __init__(self, json=None):
            self.count = 0
            self.points = 0

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

    def __init__(self):
        self.rest_client = gw2_api_client()

    def get_daily_achievements(self, tomorrow, category, lang=None):
        api_client = gw2_api_client()
        dailies = api_client.get_dailies(True if (tomorrow == "tomorrow") else False)

        daily_ids = []
        for daily in dailies[category]:
            daily_ids.append(str(daily["id"]))

        daily_details = api_client.get_daily_quest_details(",".join(daily_ids), lang)

        #bulk up item rewards lookups
        items_ids = ",".join([str(qr["id"]) for dq in daily_details for qr in dq["rewards"] if qr["type"] == "Item"])
        reward_items = self.rest_client.get_items(items_ids, lang)
        items_data = {}
        for data in reward_items:
            items_data[data["id"]] = data

        achievement_list = []
        for dailyd in daily_details:
            ach = gw2_high_level_api_client.achievement(dailyd["id"], dailyd)
            for reward in ach.rewards:
                if(reward.type == "Item"):
                    reward.item = gw2_high_level_api_client.item(items_data[reward.id])
            achievement_list.append(ach)
        return achievement_list

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
            rewards_text = ", ".join(["{} x{}".format(reward.item.name, reward.count) for reward in quest.rewards])
            em.add_field(name=quest.name, value="{}\nRewards: {}\n".format(quest.requirement, rewards_text), inline=False)

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
