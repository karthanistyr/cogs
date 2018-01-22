class icon:
    def __init__(self, json=None):
        self.id = None
        self.icon = None

        if(json is not None):
            self.load_from_json(json)

    def load_from_json(self, json):
        self.id = json.get("id", None)
        self.icon = json.get("icon", None)
