from gw2api.model.LoadableObject import LoadableObjectContainer, LoadableObjectBase

class MasteryLevel:
    def __init__(self, json=None):
        self.name = None
        self.description = None
        self.instruction = None
        self.icon = None
        self.point_cost = None
        self.exp_cost = None

        if(json is not None):
            self.populate(json)

    def populate(self, json):
        self.name = json.get("name", None)
        self.description = json.get("description", None)
        self.instruction = json.get("instruction", None)
        self.icon = json.get("icon", None)
        self.point_cost = json.get("point_cost", None)
        self.exp_cost = json.get("exp_cost", None)


class Mastery(LoadableObjectBase):
    def __init__(self, id):
        self.id = id
        self.name = None
        self.requirement = None
        self.order = None
        self.background = None
        self.region = None
        self.levels = []

    def _populate_inner(self, json):
        self.name = json.get("name", None)
        self.requirement = json.get("requirement", None)
        self.order = json.get("order", None)
        self.background = json.get("background", None)
        self.region = json.get("region", None)

        if("levels" in json):
            for level in json["levels"]:
                self.levels.append(MasteryLevel(level))
