from enum import Enum
from gw2api.model.LoadableObject import LoadableTypeEnum, LoadableObjectBase, LoadableObjectContainer
from gw2api.model.Skill import Skill

class ItemType(Enum):
    Armor = "Armor"
    BackItem = "Back"
    Bag = "Bag"
    Consumable = "Consumable"
    Container = "Container"
    CraftingMaterial = "CraftingMaterial"
    GatheringTools = "Gathering"
    Gizmo = "Gizmo"
    MiniPet = "MiniPet"
    SalvageKit = "Salvage"
    Tool = "Tool"
    Trait = "Trait"
    Trinket = "Trinket"
    Trophy = "Trophy"
    UpgradeComponent = "UpgradeComponent"
    Weapon = "Weapon"

class Item(LoadableObjectBase):
    def __init__(self, id):
        self.id = id
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
        self.chat_link = None
        self.icon = None

    def _populate_inner(self, json):
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

class InfusionSlot:
    def __init__(self, json=None):
        self.flags = []
        self.item = None

        if(json is not None):
            self._populate(json)

    def _populate(self, json):
        self.flags = json["flags"]
        if("item_id" in json):
            self.item = LoadableObjectContainer(json["item_id"], LoadableTypeEnum.Item)

class AttributeModifier:
    def __init__(self, json=None):
        self.attribute = None
        self.modifier = None

        if(json is not None):
            self._populate(json)

    def _populate(self, json):
        self.attribute = json.get("attribute", None)
        self.modifier = json.get("modifier", None)

class Buff:
    def __init__(self, json=None):
        self.attribute = None
        self.modifier = None

        if(json is not None):
            self._populate(json)

    def _populate(self, json):
        self.skill = LoadableObjectContainer(json["skill_id"], LoadableTypeEnum.Skill)
        self.description = json.get("description", None)

class InfixUpgrade:
    def __init__(self, json=None):
        self.id = None
        self.attributes = []
        self.buff = None

        if(json is not None):
            self._populate(json)

    def _populate(self, json):
        self.id = json.get("id", None)
        for attr_mod_data in json["attributes"]:
            self.attributes.append(AttributeModifier(attr_mod_data))
        if("buff" in json):
            self.buff = Buff(json["buff"])

class ItemStat(LoadableObjectBase):
    def __init__(self, id):
        self.id = id
        self.name = None
        self.attributes = []

    def _populate_inner(self, json):
        self.name = json.get("name", None)
        for attr_mod_data in json["attributes"]:
            self.attributes.append(AttributeModifier({attr_mod_data: json["attributes"][attr_mod_data]}))

class HasInfusion:
    def __init__(self):
        self.infusion_slots = []

    def populate(self, json):
        if("infusion_slots" in json):
            for infusion_slot_data in json["infusion_slots"]:
                self.infusion_slots.append(InfusionSlot(infusion_slot_data))

class HasInfixUpgrade:
    def __init__(self):
        self.infix_upgrade = None

    def populate(self, json):
        if("infix_upgrade" in json):
            self.infix_upgrade = InfixUpgrade(json["infix_upgrade"])

class HasSuffix:
    def __init__(self):
        self.suffix_item = None

    def populate(self, json):
        if("suffix_item_id" in json):
            self.suffix_item = LoadableObjectContainer(json["suffix_item_id"], LoadableTypeEnum.Item)

class HasStatChoices:
    def __init__(self):
        self.stat_choices = []

    def populate(self, json):
        if("stat_choices" in json):
            for stat_choice_data in json["stat_choices"]:
                self.stat_choices.append(LoadableObjectContainer(stat_choice_data, LoadableTypeEnum.ItemStat))

class Armor(Item, HasInfusion, HasInfixUpgrade, HasSuffix, HasStatChoices):
    def __init__(self, id):
        Item.__init__(self, id)
        HasInfusion.__init__(self)
        HasInfixUpgrade.__init__(self)
        HasSuffix.__init__(self)
        HasStatChoices.__init__(self)

        self.subtype = None # item details "type" in the API
        self.weight_class = None
        self.defense = None

    def _populate_inner(self, json):
        super()._populate_inner(json)
        details_json = json["details"]

        self.subtype = details_json.get("type", None)
        self.weight_class = details_json.get("weight_class", None)
        self.defense = details_json.get("defense", None)

        HasInfusion.populate(self, details_json)
        HasInfixUpgrade.populate(self, details_json)
        HasSuffix.populate(self, details_json)
        HasStatChoices.populate(self, details_json)

class BackItem(Item, HasInfusion, HasInfixUpgrade, HasSuffix, HasStatChoices):
    def __init__(self, id):
        Item.__init__(self, id)
        HasInfusion.__init__(self)
        HasInfixUpgrade.__init__(self)
        HasSuffix.__init__(self)
        HasStatChoices.__init__(self)

    def _populate_inner(self, json):
        super()._populate_inner(json)
        details_json = json["details"]

        HasInfusion.populate(self, details_json)
        HasInfixUpgrade.populate(self, details_json)
        HasSuffix.populate(self, details_json)
        HasStatChoices.populate(self, details_json)

class Bag(Item):
    def __init__(self, id):
        Item.__init__(self, id)

        self.size = None
        self.no_sell_or_sort = None

    def _populate_inner(self, json):
        super()._populate_inner(json)
        details_json = json["details"]

        self.size = details_json.get("size", None)
        self.no_sell_or_sort = details_json.get("no_sell_or_sort", None)

class Consumable(Item):
    def __init__(self, id):
        Item.__init__(self, id)

        self.subtype = None
        self.description = None
        self.duration_ms = None
        self.unlock_type = None
        self.color_id = None
        self.recipe_id = None
        self.apply_count = None
        self.name = None

    def _populate_inner(self, json):
        super()._populate_inner(json)
        details_json = json["details"]

        self.subtype = details_json.get("type", None)
        self.description = details_json.get("description", None)
        self.duration_ms = details_json.get("duration_ms", None)
        self.unlock_type = details_json.get("unlock_type", None)
        self.color_id = details_json.get("color_id", None)
        self.recipe_id = details_json.get("recipe_id", None)
        self.apply_count = details_json.get("apply_count", None) # API docs don't give a description for this
        self.name = details_json.get("name", None)

class Container(Item):
    def __init__(self, id):
        Item.__init__(self, id)

        self.subtype = None

    def _populate_inner(self, json):
        super()._populate_inner(json)
        details_json = json["details"]

        self.subtype = details_json.get("type", None)

class GatheringTools(Item):
    def __init__(self, id):
        Item.__init__(self, id)

        self.subtype = None

    def _populate_inner(self, json):
        super()._populate_inner(json)
        details_json = json["details"]

        self.subtype = details_json.get("type", None)

class Gizmo(Item):
    def __init__(self, id):
        Item.__init__(self, id)

        self.subtype = None

    def _populate_inner(self, json):
        super()._populate_inner(json)
        details_json = json["details"]

        self.subtype = details_json.get("type", None)

class MiniPet(Item):
    def __init__(self, id):
        Item.__init__(self, id)

        self.minipet = None

    def _populate_inner(self, json):
        super()._populate_inner(json)
        details_json = json["details"]

        self.minipet = LoadableObjectContainer(json["minipet_id"], LoadableTypeEnum.MiniPet)

class SalvageKit(Item):
    def __init__(self, id):
        Item.__init__(self, id)

        self.subtype = None
        self.charges = None

    def _populate_inner(self, json):
        super()._populate_inner(json)
        details_json = json["details"]

        self.subtype = details_json.get("type", None)
        self.charges = details_json.get("charges", None)

class Trinket(Item, HasInfusion, HasInfixUpgrade, HasSuffix, HasStatChoices):
    def __init__(self, id):
        Item.__init__(self, id)
        HasInfusion.__init__(self)
        HasInfixUpgrade.__init__(self)
        HasSuffix.__init__(self)
        HasStatChoices.__init__(self)

        self.subtype = None # item details "type" in the API

    def _populate_inner(self, json):
        super()._populate_inner(json)

        details_json = json["details"]

        self.subtype = details_json.get("type", None)
        self.damage_type = details_json.get("damage_type", None)
        self.min_power = details_json.get("min_power", None)
        self.max_power = details_json.get("max_power", None)
        self.defense = details_json.get("defense", None)

        HasInfusion.populate(self, details_json)
        HasInfixUpgrade.populate(self, details_json)
        HasSuffix.populate(self, details_json)
        HasStatChoices.populate(self, details_json)

class UpgradeComponent(Item, HasInfixUpgrade):
    def __init__(self, id):
        Item.__init__(self, id)
        HasInfixUpgrade.__init__(self)

        self.subtype = None
        self.flags = []
        self.infusion_upgrade_flags = []
        self.suffix = None

    def _populate_inner(self, json):
        super()._populate_inner(json)

        details_json = json["details"]

        self.subtype = details_json.get("type", None)
        self.suffix = details_json.get("suffix", None)
        for flag in details_json["flags"]:
            self.flags.append(flag)
        for infusion_upgrade_flag in details_json["infusion_upgrade_flags"]:
            self.infusion_upgrade_flags.append(infusion_upgrade_flag)

        HasInfixUpgrade.populate(self, details_json)

class Weapon(Item, HasInfusion, HasInfixUpgrade, HasSuffix, HasStatChoices):
    def __init__(self, id):
        Item.__init__(self, id)
        HasInfusion.__init__(self)
        HasInfixUpgrade.__init__(self)
        HasSuffix.__init__(self)
        HasStatChoices.__init__(self)

        self.subtype = None # item details "type" in the API
        self.damage_type = None
        self.min_power = None
        self.max_power = None
        self.defense = None

    def _populate_inner(self, json):
        super()._populate_inner(json)

        details_json = json["details"]

        self.subtype = details_json.get("type", None)
        self.damage_type = details_json.get("damage_type", None)
        self.min_power = details_json.get("min_power", None)
        self.max_power = details_json.get("max_power", None)
        self.defense = details_json.get("defense", None)

        HasInfusion.populate(self, details_json)
        HasInfixUpgrade.populate(self, details_json)
        HasSuffix.populate(self, details_json)
        HasStatChoices.populate(self, details_json)
