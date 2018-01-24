from gw2api.model.LoadableObject import LoadableObjectBase, LoadableTypeEnum
from gw2api.model.Crafting import Crafting
from gw2api.model.Inventory import *

class Character(LoadableObjectBase):
    def __init__(self, name):
        self.name = name
        self.id = name
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
        self.equipment = {}
        self.bags = []
        self.recipes = []
        self.equipment_pvp = []
        self.training = []

    def _populate_inner(self, json):
        self.race = json.get("race", None)
        self.gender = json.get("gender", None)
        self.flags = []
        self.profession = json.get("profession", None)
        self.level = json.get("level", None)
        self.guild = None # TODO guilde
        self.age = json.get("age", None)
        self.created = json.get("created", None)
        self.deaths = json.get("deaths", None)

        if("crafting" in json):
            for crafting_data in json["crafting"]:
                self.crafting.append(Crafting(crafting_data))

        if("title" in json):
            self.title = LoadableObjectContainer(json["title"], LoadableTypeEnum.Title)

        self.backstory = []
        self.wvw_abilities = []
        self.specializations = []
        self.skills = []

        if("equipment" in json):
            for equipment_data in json["equipment"]:
                self.equipment[equipment_data["slot"]] = EquipmentItem(equipment_data)

        if("bags" in json):
            for bag_data in json["bags"]:
                self.bags.append(InventoryBag(bag_data))

        self.recipes = []
        self.equipment_pvp = []
        self.training = []
