from gw2api.model.Item import *
from gw2api.model.Skill import Skill
from gw2api.model.Gw2LoadableObject import LoadableObjectContainer, LoadableObjectVisitorBase
from gw2api.client.gw2_api_v2_client import gw2_api_v2_client

class StubObjectsTracker(LoadableObjectVisitorBase):
    """Tracks model objects that haven't been fully loaded yet"""

    def __init__(self):
        self.items =  {}

    def collect(self, obj: LoadableObjectContainer):
        self.items["{}_{}".format(obj.loadable_type, obj.id)] = obj

class querier:

    def __init__(self):
        self.rest_client = gw2_api_v2_client()
        self.tracker = StubObjectsTracker()
        LoadableObjectContainer.register_visitor(self.tracker)

    def _get_skills(self, ids, lang=None):
        skills_data = self.rest_client.get_skills(ids, lang)
        returned_items = []
        if(skills_data is not None and len(skills_data) > 0):
            for skill_data in skills_data:
                skill = Skill(skill_data["id"])
                skill.populate(skill_data)
                returned_items.append(skill)

        return returned_items

    def _get_items(self, ids, lang=None):
        items_data = self.rest_client.get_items(ids, lang)

        returned_items = []
        if(len(items_data) > 0):
            for item_data in items_data:
                item = None
                if(item_data["type"] == ItemType.Armor.value):
                    item = Armor(item_data["id"])
                if(item_data["type"] == ItemType.BackItem.value):
                    item = BackItem(item_data["id"])
                if(item_data["type"] == ItemType.Bag.value):
                    item = Bag(item_data["id"])
                if(item_data["type"] == ItemType.Consumable.value):
                    item = Consumable(item_data["id"])
                if(item_data["type"] == ItemType.GatheringTools.value):
                    item = GatheringTools(item_data["id"])
                if(item_data["type"] == ItemType.Gizmo.value):
                    item = Gizmo(item_data["id"])
                if(item_data["type"] == ItemType.SalvageKit.value):
                    item = SalvageKit(item_data["id"])
                if(item_data["type"] == ItemType.Trinket.value):
                    item = Trinket(item_data["id"])
                if(item_data["type"] == ItemType.UpgradeComponent.value):
                    item = UpgradeComponent(item_data["id"])
                if(item_data["type"] == ItemType.Weapon.value):
                    item = Weapon(item_data["id"])

                item.populate(item_data)

                returned_items.append(item)

        return returned_items

    def _depth_fetch(func):
        def wrapper(self, ids, lang=None):

            def fetch_and_correlate(containers: dict, fetch_func):
                item_ids = ",".join([str(loadable_items[item].id) for item in loadable_items])
                api_items = fetch_func(item_ids, lang)
                api_items_dict = {}
                for api_item in api_items:
                    api_items_dict[api_item.id] = api_item

                for api_item_id in api_items_dict:
                    loadable_items[api_item_id].object = api_items_dict[api_item_id]

            to_return = func(self, ids, lang)
            while len(self.tracker.items) > 0:
                items_to_load = self.tracker.items
                self.tracker.items = {}

                # one collection for known loadable type
                loadable_items = {}
                loadable_skills = {}
                loadable_achievements = {}
                loadable_masteries = {}
                loadable_titles = {}

                #populate the collections
                for index in items_to_load:
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Item):
                        loadable_items[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Skill):
                        loadable_skills[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Achievement):
                        loadable_achievements[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Title):
                        loadable_titles[items_to_load[index].id] = items_to_load[index]
                    if(items_to_load[index].loadable_type == LoadableTypeEnum.Mastery):
                        loadable_masteries[items_to_load[index].id] = items_to_load[index]

                #bulk fetch items
                if(len(loadable_items) > 0):
                    fetch_and_correlate(loadable_items, self._get_items)

                #bulk fetch skills
                if(len(loadable_skills) > 0):
                    fetch_and_correlate(loadable_items, self._get_skills)

            return to_return
        return wrapper

    @_depth_fetch
    def get_skills(self, ids, lang=None):
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
