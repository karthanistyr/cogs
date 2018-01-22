import requests
import urllib

class gw2_api_v2_client:
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

    def get_skills(self, ids, lang=None):
        ep_skills = "/v2/skills"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        skills = self.get_request(ep_skills, args)
        return skills

    def get_masteries(self, ids, lang=None):
        ep_masteries = "/v2/masteries"
        args = {"ids": ids}

        if(lang is not None):
            args["lang"] = lang

        masteries = self.get_request(ep_masteries, args)
        return masteries
