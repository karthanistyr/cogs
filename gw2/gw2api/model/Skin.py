from gw2api.model.LoadableObject import LoadableObjectBase, LoadableTypeEnum

class Skin(LoadableObjectBase):
    def __init__(self, id):
        self.id = id
        self.name = None
        self.type = None
        self.flags = []
        self.restrictions = None
        self.icon = None
        self.rarity = None
        self.description = None

    def _populate_inner(self, json):
        self.name = json.get("name", None)
        self.type = json.get("type", None)
        self.flags = json.get("flags", None)
        self.restrictions = json.get("restrictions", None)
        self.icon = json.get("icon", None)
        self.rarity = json.get("rarity", None)
        self.description = json.get("description", None)
