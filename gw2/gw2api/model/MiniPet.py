from gw2api.model.LoadableObject import LoadableObjectBase

class MiniPet(LoadableObjectBase):
    def __init__(self, id):
        self.id = id
        self.name = None
        self.icon = None
        self.order = None
        self.item_id = None

    def _populate_inner(self, json):
        self.name = json.get("name", None)
        self.icon = json.get("icon", None)
        self.order = json.get("order", None)
        self.item_id = json.get("item_id", None) #not depth-loading this as it's circular with the Item itself
