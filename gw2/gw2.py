import discord
import datetime
import re
from enum import Enum
from .utils.dataIO import dataIO
from discord.ext import commands
from gw2api.Query import Querier

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

    def get_guild_key(self, guild_acronym):
        keys = self.loadGuildKeys()
        if(guild_acronym in keys):
            return keys[guild_acronym]

    def translate_log_entry(self, log_entry):
        if(log_entry.type == "joined"):
            return "[{}] {}".format(log_entry.time, self.strings["log_entry_joined_mask"].format(new_joiner=log_entry.user))
        if(log_entry.type == "invited"):
            return "[{}] {}".format(log_entry.time, self.strings["log_entry_invited_mask"].format(invited=log_entry.user, recruiter=log_entry.invited_by))
        if(log_entry.type == "kicked"):
            return "[{}] {}".format(log_entry.time, self.strings["log_entry_kicked_mask"].format(kicked=log_entry.user, kicker=log_entry.kicked_by))
        if(log_entry.type == "rank_change"):
            return "[{}] {}".format(log_entry.time, self.strings["log_entry_rankchange_mask"].format(changed=log_entry.user, changer=log_entry.changed_by, old_rank=log_entry.old_rank, new_rank=log_entry.new_rank))
        if(log_entry.type == "treasury"):
            return "[{}] {}".format(log_entry.time, self.strings["log_entry_treasury_mask"].format(donator=log_entry.user, item_name=log_entry.item.id, quantity=log_entry.count))
        if(log_entry.type == "stash"):
            return "[{}] {}".format(log_entry.time, self.strings["log_entry_stash_mask"].format(member=log_entry.user, action=self.strings[log_entry.operation], item_name=self.strings["gold"] if log_entry.item is None else log_entry.item.id, quantity=log_entry.count))
        if(log_entry.type == "motd"):
            return "[{}] {}".format(log_entry.time, self.strings["log_entry_motd_mask"].format(officer=log_entry.user, motd=log_entry.motd))
        if(log_entry.type == "upgrade"):
            return "[{}] {}".format(log_entry.time, self.strings["log_entry_upgrade_mask"].format(member=log_entry.user, action=log_entry.action, upgrade_name=log_entry.upgrade.object.name))
        if(log_entry.type == "influence"):
            return "[{}] {}".format(log_entry.time, self.strings["log_entry_influence_mask"].format(nb_participants=log_entry.total_participants, activity=self.strings[log_entry.activity], participants=", ".join(log_entry.participants)))
        return str(log_entry)

    async def bot_say_large_text(self, large_text):
        message_char_limit = 2000
        remaining_string = large_text
        while(len(remaining_string) > 0):
            buffer = remaining_string[:message_char_limit]
            remaining_string = remaining_string[message_char_limit:]
            await self.bot.say(buffer)

    @commands.command()
    async def guild(self, guild_acronym, guild_command, nb_lines=10):

        async def display_guild_details(guild_details):
            if(not guild_details.has_loaded):
                return
            em = discord.Embed(title=guild_details.object.name,
                color=int("0x{}".format(guild_details.object.id[:6]), 16),
                description=guild_details.object.motd)
            em.add_field(name=self.strings["favour"], value=guild_details.object.favor, inline=True)
            em.add_field(name=self.strings["influence"], value=guild_details.object.influence, inline=True)
            em.add_field(name=self.strings["aetherium"], value=guild_details.object.aetherium, inline=True)
            em.add_field(name=self.strings["tag"], value=guild_details.object.tag, inline=True)
            await self.bot.say(embed=em)

        async def display_log_lines(log_lines):
            all_lines = "\n".join([self.translate_log_entry(log_line) for log_line in log_lines])
            await self.bot_say_large_text(all_lines)

        if(not self.validate_string_input(guild_acronym)):
            await self.bot.say(self.strings["wrong_guild_alias_format"])
            return

        guild_creds = self.get_guild_key(guild_acronym)
        if(guild_creds is None):
            await self.bot.say(self.strings["no_key_exists"])
            return

        api_client = Querier()

        #switch command
        if(guild_command == "details"):
            guild_details_data = api_client.get_guild(guild_creds["guild_id"], self.locale, guild_creds["api_key"])
            if(not guild_details_data.has_loaded):
                raise AssertionError(self.strings["guild_name_not_found"])
            await display_guild_details(guild_details_data)
            return
        elif(guild_command == "log"):
            if(nb_lines > 30):
                await self.bot.say(self.strings["max_log_lines_exceeded"].format(30))
                return

            log_lines = api_client.get_guild_log(guild_creds["guild_id"], guild_creds["api_key"], nb_lines)
            if(log_lines is not None and len(log_lines) > 0):
                await display_log_lines(log_lines)
                return

            await self.bot.say(self.strings["no_log_to_display"])
        else:
            await self.bot.say(self.strings["unknown_command"])
            return

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

        em = discord.Embed(title="_{}_".format(char.object.title.object.name if (char.object.title is not None and char.object.title.has_loaded) else self.strings["titleless"]),
            color=char.object.deaths)
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
    async def storeguildkey(self, guild_full_name, guild_acronym, api_key=None):
        if(api_key is None):
            await self.bot.say(self.strings["no_key_passed"])
            return

        if(not self.validate_api_key_format(api_key)):
            await self.bot.say(self.strings["wrong_key_format"])
            return

        if(not self.validate_string_input(guild_full_name, 3, 50, "[\w ]")):
            await self.bot.say(self.strings["wrong_guild_alias_format"])
            return

        if(not self.validate_string_input(guild_acronym)):
            await self.bot.say(self.strings["wrong_guild_alias_format"])
            return

        keys = self.loadGuildKeys()

        if(guild_acronym in keys):
            await self.bot.say(self.strings["key_exists_warning"])
        else:
            api_client = Querier()
            guild_id = api_client.get_guild_id(guild_full_name)
            if(guild_id is None):
                await self.bot.say(self.strings["guild_name_not_found"])
                return

            staging_data = {"guild_id": guild_id, "api_key": api_key}
            keys[guild_acronym] = staging_data

            self.write_guild_keys(keys)
            await self.bot.say(self.strings["command_completed"])

    @commands.command()
    async def deleteguildkey(self, guild_acronym):
        if(not self.validate_string_input(guild_acronym)):
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
