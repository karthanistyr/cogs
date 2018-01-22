class AchievementTier:
    def __init__(self, json=None):
        self.count = None
        self.points = None

        if(json is not None):
            self.load_from_json(json)

    def load_from_json(self, json: dict):
        self.count = json.get("count", None)
        self.points = json.get("points", None)
