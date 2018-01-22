class Crafting:
    def __init__(self, json=None):
        self.discipline = None
        self.rating = None
        self.active = None

        if(json is not None):
            self.load_from_json(json)

    def load_from_json(self, json: dict):
        self.discipline = json.get("discipline", None)
        self.rating = json.get("rating", None)
        self.active = json.get("active", None)
