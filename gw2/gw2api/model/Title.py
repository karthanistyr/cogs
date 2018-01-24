from gw2api.model.LoadableObject import LoadableObjectBase

class Title(LoadableObjectBase):
    def __init__(self, id):
        self.id = id
        self.name = None

    def _populate_inner(self, json):
        self.name = json.get("name", None)
