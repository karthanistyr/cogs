from gw2api.model.Achievement import Achievement
from gw2api.model.Item import *
from gw2api.model.Mastery import Mastery
from gw2api.model.MiniPet import MiniPet
from gw2api.model.Skill import Skill
from gw2api.model.Skin import Skin
from gw2api.model.Title import Title
from gw2api.model.Character import Character
from gw2api.model.Guild import Guild

from gw2api.model.LoadableObject import LoadableObjectContainer, LoadableObjectVisitorBase
from gw2api.client.Gw2RestClient import Gw2RestClient

class StubObjectsTracker(LoadableObjectVisitorBase):
    """Tracks model objects that haven't been fully loaded yet"""

    def __init__(self):
        self.items =  {}

    def collect(self, obj: LoadableObjectContainer):
        self.items["{}_{}".format(obj.loadable_type, obj.id)] = obj

class Querier:

    def __init__(self):
        self.rest_client = Gw2RestClient()
        self.tracker = StubObjectsTracker()
        LoadableObjectContainer.register_visitor(self.tracker)

    def privileged(func):
        func.__dict__["privileged"] = True
        return func

    @privileged
    def _get_character(self, name, lang, api_key):
        character_data = self.rest_client.get_characters(api_key, name)
        returned_items = []
        if(character_data is not None):
            char = Character(character_data["name"])
            char.populate(character_data)
            returned_items.append(char)

        return returned_items

    @privileged
    def _get_characters(self, name, lang, api_key):
        character_names = self.rest_client.get_characters(api_key)
        return character_names

    @privileged
    def _get_guild(self, id, api_key):
        guild_data = self.rest_client.get_guild(id, api_key)

        guild = None
        if(guild_data is not None):
            guild = Guild(id)
            guild.populate(guild_data)

        return guild

    def _get_itemstats(self, ids, lang=None):
        itemstats_data = self.rest_client.get_itemstats(ids, lang)
        returned_items = []
        if(itemstats_data is not None and len(itemstats_data) > 0):
            for itemstat_data in itemstats_data:
                itemstat = ItemStat(itemstat_data["id"])
                itemstat.populate(itemstat_data)
                returned_items.append(itemstat)

        return returned_items

    def _get_masteries(self, ids, lang=None):
        masteries_data = self.rest_client.get_masteries(ids, lang)
        returned_items = []
        if(masteries_data is not None and len(masteries_data) > 0):
            for mastery_data in masteries_data:
                mastery = Mastery(mastery_data["id"])
                mastery.populate(mastery_data)
                returned_items.append(mastery)

        return returned_items

    def _get_titles(self, ids, lang=None):
        titles_data = self.rest_client.get_titles(ids, lang)
        returned_items = []
        if(titles_data is not None and len(titles_data) > 0):
            for title_data in titles_data:
                title = Title(title_data["id"])
                title.populate(title_data)
                returned_items.append(title)

        return returned_items

    def _get_skills(self, ids, lang=None):
        skills_data = self.rest_client.get_skills(ids, lang)
        returned_items = []
        if(skills_data is not None and len(skills_data) > 0):
            for skill_data in skills_data:
                skill = Skill(skill_data["id"])
                skill.populate(skill_data)
                returned_items.append(skill)

        return returned_items

    def _get_skins(self, ids, lang=None):
        skins_data = self.rest_client.get_skins(ids, lang)
        returned_items = []
        if(skins_data is not None and len(skins_data) > 0):
            for skin_data in skins_data:
                skin = Skin(skin_data["id"])
                skin.populate(skin_data)
                returned_items.append(skin)

        return returned_items

    def _get_minis(self, ids, lang=None):
        minis_data = self.rest_client.get_minis(ids, lang)
        returned_items = []
        if(minis_data is not None and len(minis_data) > 0):
            for mini_data in minis_data:
                mini = MiniPet(mini_data["id"])
                mini.populate(mini_data)
                returned_items.append(mini)

        return returned_items

    def _get_items(self, ids, lang=None):
        items_data = self.rest_client.get_items(ids, lang)

        returned_items = []
        if(items_data is not None and len(items_data) > 0):
            for item_data in items_data:
                item = None
                if(item_data["type"] == ItemType.Armor.value):
                    item = Armor(item_data["id"])
                elif(item_data["type"] == ItemType.BackItem.value):
                    item = BackItem(item_data["id"])
                elif(item_data["type"] == ItemType.Bag.value):
                    item = Bag(item_data["id"])
                elif(item_data["type"] == ItemType.Consumable.value):
                    item = Consumable(item_data["id"])
                elif(item_data["type"] == ItemType.Container.value):
                    item = Container(item_data["id"])
                elif(item_data["type"] == ItemType.GatheringTools.value):
                    item = GatheringTools(item_data["id"])
                elif(item_data["type"] == ItemType.Gizmo.value):
                    item = Gizmo(item_data["id"])
                elif(item_data["type"] == ItemType.MiniPet.value):
                    item = MiniPet(item_data["id"])
                elif(item_data["type"] == ItemType.SalvageKit.value):
                    item = SalvageKit(item_data["id"])
                elif(item_data["type"] == ItemType.Trinket.value):
                    item = Trinket(item_data["id"])
                elif(item_data["type"] == ItemType.UpgradeComponent.value):
                    item = UpgradeComponent(item_data["id"])
                elif(item_data["type"] == ItemType.Weapon.value):
                    item = Weapon(item_data["id"])
                else:
                    item = Item(item_data["id"])

                item.populate(item_data)
                returned_items.append(item)

        return returned_items

    def _get_achievements(self, ids, lang=None):
        achievements_data = self.rest_client.get_achievements(ids, lang)

        returned_items = []
        if(achievements_data is not None and len(achievements_data) > 0):
            for achievement_data in achievements_data:
                achievement = Achievement(achievement_data["id"])
                achievement.populate(achievement_data)
                returned_items.append(achievement)

        return returned_items

    def _depth_fetch(func):
        def wrapper(self, ids, lang=None, api_key=None):

            def fetch_and_correlate(containers: dict, fetch_func):
                item_ids = ",".join([str(containers[item].id) for item in containers])
                api_items = []
                if(fetch_func.__dict__.get("privileged", False) == True):
                    api_items = fetch_func(item_ids, lang, api_key)
                else:
                    api_items = fetch_func(item_ids, lang)
                api_items_dict = {}
                for api_item in api_items:
                    api_items_dict[api_item.id] = api_item

                for api_item_id in api_items_dict:
                    containers[api_item_id].object = api_items_dict[api_item_id]

            to_return = func(self, ids, lang)
            while len(self.tracker.items) > 0:
                items_to_load = self.tracker.items
                self.tracker.items = {}

                # one collection for known loadable type
                loadable_items = {}
                loadable_itemstats = {}
                loadable_skills = {}
                loadable_skins = {}
                loadable_achievements = {}
                loadable_masteries = {}
                loadable_titles = {}
                loadable_characters = {}
                loadable_guilds = {}
                loadable_guildupgrades = {}

                #populate the collections
                for index in items_to_load:
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Item):
                        loadable_items[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.ItemStat):
                        loadable_itemstats[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Skill):
                        loadable_skills[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Skin):
                        loadable_skins[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Achievement):
                        loadable_achievements[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Title):
                        loadable_titles[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Mastery):
                        loadable_masteries[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Character):
                        loadable_characters[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Guild):
                        loadable_guilds[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.GuildUpgrade):
                        loadable_guildupgrades[items_to_load[index].id] = items_to_load[index]


                #bulk fetch items
                if(len(loadable_items) > 0):
                    fetch_and_correlate(loadable_items, self._get_items)

                #bulk fetch items
                if(len(loadable_itemstats) > 0):
                    fetch_and_correlate(loadable_itemstats, self._get_itemstats)

                #bulk fetch skills
                if(len(loadable_skills) > 0):
                    fetch_and_correlate(loadable_skills, self._get_skills)

                #bulk fetch skills
                if(len(loadable_skins) > 0):
                    fetch_and_correlate(loadable_skins, self._get_skins)

                #bulk fetch achievements
                if(len(loadable_achievements) > 0):
                    fetch_and_correlate(loadable_achievements, self._get_achievements)

                #bulk fetch titles
                if(len(loadable_titles) > 0):
                    fetch_and_correlate(loadable_titles, self._get_titles)

                #bulk fetch masteries
                if(len(loadable_masteries) > 0):
                    fetch_and_correlate(loadable_masteries, self._get_masteries)

                #bulk fetch characters
                if(len(loadable_characters) > 0):
                    fetch_and_correlate(loadable_characters, self._get_character)

            return to_return
        return wrapper

    @_depth_fetch
    def get_character(self, name, lang=None, api_key=None):
        return LoadableObjectContainer(name, LoadableTypeEnum.Character)

    def get_characters(self, api_key):
        return self._get_characters(None, None, api_key)

    @_depth_fetch
    def get_masteries(self, ids, lang=None):
        returned_items = []
        for id in ids:
            returned_items.append(LoadableObjectContainer(id, LoadableTypeEnum.Mastery))
        return returned_items

    @_depth_fetch
    def get_itemstats(self, ids, lang=None):
        returned_items = []
        for id in ids:
            returned_items.append(LoadableObjectContainer(id, LoadableTypeEnum.ItemStat))
        return returned_items

    @_depth_fetch
    def get_titles(self, ids, lang=None):
        returned_items = []
        for id in ids:
            returned_items.append(LoadableObjectContainer(id, LoadableTypeEnum.Title))
        return returned_items

    @_depth_fetch
    def get_achievements(self, ids, lang=None):
        returned_items = []
        for id in ids:
            returned_items.append(LoadableObjectContainer(id, LoadableTypeEnum.Achievement))
        return returned_items

    @_depth_fetch
    def get_skills(self, ids, lang=None):
        returned_items = []
        for id in ids:
            returned_items.append(LoadableObjectContainer(id, LoadableTypeEnum.Skin))
        return returned_items

    @_depth_fetch
    def get_skins(self, ids, lang=None):
        returned_items = []
        for id in ids:
            returned_items.append(LoadableObjectContainer(id, LoadableTypeEnum.Skill))
        return returned_items

    @_depth_fetch
    def get_items(self, ids, lang=None):
        returned_items = []
        for id in ids:
            returned_items.append(LoadableObjectContainer(id, LoadableTypeEnum.Item))
        return returned_items
