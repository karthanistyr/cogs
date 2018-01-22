from gw2api.model.Gw2LoadableObject import LoadableObjectBase

class Title(LoadableObjectBase):
    def __init__(self, id):
        self.id = id
        self.name = None

        if(json is not None):
            self.load_from_json(json)

    def _populate_inner(self, json):
        self.name = json.get("name", None)
