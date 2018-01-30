import requests
import urllib

class Gw2RestClient:
    def __init__(self):
        self.root_api_endpoint = "https://api.guildwars2.com"

    def validate_id_string(self):
        regexp = "([\d]+,?)*\d+"
        # TODO: complete regex validation

    def get_request(self, endpoint, arguments, api_key=None):
        complete_endpoint = self.root_api_endpoint + endpoint
        headers = None

        if(api_key is not None):
            headers = {"Authorization": "Bearer {}".format(api_key)}

        get_response = requests.get(complete_endpoint, params=arguments, headers=headers)

        if(get_response.status_code == 200):
            return get_response.json()

    def get_file_list(self, ids=None):
        ep_files = "/v2/files"
        args = {"ids": "all" if ids is None else ids}

        files_data = self.get_request(ep_files, args)
        return files_data

    def get_characters(self, api_key, char_name=None):
        ep = "/v2/characters"

        safe_char_name = ""
        if(char_name is not None):
            safe_char_name = urllib.parse.quote(char_name)

        char_data = self.get_request(ep + "/" + safe_char_name, None, api_key)
        return char_data

    def get_dailies(self, tomorrow: bool=False):
        ep_today = "/v2/achievements/daily"
        ep_tomorrow = ep_today + "/tomorrow"

        dailies_data = self.get_request(ep_tomorrow if tomorrow else ep_today, None)
        return dailies_data

    def get_masteries(self, ids, lang=None):
        ep_masteries = "/v2/masteries"
        args = {"ids": ids}

        if(lanf is not None):
            args["lang"] = lang

        masteries_data = self.get_request(ep_masteries, args)
        return masteries_data

    def get_achievements(self, ids, lang=None):
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

    def get_itemstats(self, ids, lang=None):
        ep_itemstats = "/v2/itemstats"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        itemstats_data = self.get_request(ep_itemstats, args)
        return itemstats_data

    def get_titles(self, ids, lang=None):
        ep_titles = "/v2/titles"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        titles = self.get_request(ep_titles, args)
        return titles

    def get_skills(self, ids, lang=None):
        ep_skills = "/v2/skills"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        skills = self.get_request(ep_skills, args)
        return skills

    def get_skins(self, ids, lang=None):
        ep_skins = "/v2/skins"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        skins = self.get_request(ep_skins, args)
        return skins

    def get_masteries(self, ids, lang=None):
        ep_masteries = "/v2/masteries"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        masteries = self.get_request(ep_masteries, args)
        return masteries

    def get_minis(self, id, lang=None):
        ep_minis = "/v2/minis"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        minis_data = self.get_request(ep_minis, args)
        return minis_data

    def get_guild(self, id, api_key):
        ep_guild = "/v2/guild/{}"

        guild_data = self.get_request(ep_guild.format(id), None, api_key)
        return guild_data

    def get_guild_log(self, id, api_key, nb_lines=None):
        ep_guild_log = "/v2/guild/{}/log"

        log_data = self.get_request(ep_guild_log.format(id), None, api_key)
        if(nb_lines is not None):
            log_data = log_data[:nb_lines]

        return log_data
