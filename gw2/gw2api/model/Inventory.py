from gw2api.model.LoadableObject import LoadableObjectContainer, LoadableTypeEnum

class InventoryBag:
    def __init__(self, json=None):
        self.item = None
        self.size = None
        self.inventory = []

        if(json is not None):
            self.populate(json)

    def populate(self, json):
        self.item = LoadableObjectContainer(json["id"], LoadableTypeEnum.Item)
        self.size = json.get("size", None)

        for inv_item_data in json["inventory"]:
            if(inv_item_data is not None):
                self.inventory.append(InventoryItem(inv_item_data))

class InventoryItem:
    def __init__(self, json=None):
        self.item = None
        self.count = None
        self.infusions = []
        self.upgrades = []
        self.skin = None
        self.stats = None
        self.binding = None
        self.bound_to = None

        if(json is not None):
            self.populate(json)

    def populate(self, json):
        self.item = LoadableObjectContainer(json["id"], LoadableTypeEnum.Item)
        self.count = json.get("count", None)

        if("skin" in json):
            self.skin = LoadableObjectContainer(json["skin"], LoadableTypeEnum.Skin)

        if("infusions" in json):
            for infusion in json["infusions"]:
                self.infusions.append(LoadableObjectContainer(infusion, LoadableTypeEnum.Item))

        if("upgrades" in json):
            for upgrade in json["upgrades"]:
                self.upgrades.append(LoadableObjectContainer(upgrade, LoadableTypeEnum.Item))

        if("stats" in json):
            self.stats = LoadableObjectContainer(json["stats"]["id"], LoadableTypeEnum.ItemStat)

        if("binding" in json):
            self.binding = json.get("binding", None)

        if("bound_to" in json):
            self.bound_to = json.get("bound_to", None)

class EquipmentItem(InventoryItem):
    def __init__(self, json=None):
        self.slot = None
        super().__init__(json)

    def populate(self, json):
        self.slot = json.get("slot", None)
        super().populate(json)
