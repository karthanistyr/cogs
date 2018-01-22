class character:
    def __init__(self, json=None):
        self.name = None
        self.race = None
        self.gender = None
        self.flags = []
        self.profession = None
        self.level = None
        self.guild = None
        self.age = None
        self.created = None
        self.deaths = None
        self.crafting = []
        self.title = None
        self.backstory = []
        self.wvw_abilities = []
        self.specializations = []
        self.skills = []
        self.equipement = []
        self.recipes = []
        self.equipment_pvp = []
        self.training = []

        if(json is not None):
            self.load_from_json(json)

    def load_from_json(self, json: dict):
        self.name = json.get("name", None)
        self.race = json.get("race", None)
        self.gender = json.get("gender", None)
        self.flags = []
        self.profession = json.get("profession", None)
        self.level = json.get("level", None)
        self.guild = None # TODO guilde
        self.age = json.get("age", None)
        self.created = json.get("created", None)
        self.deaths = json.get("deaths", None)
        self.crafting = []
        self.title = None # TODO title
        self.backstory = []
        self.wvw_abilities = []
        self.specializations = []
        self.skills = []
        self.equipement = []
        self.recipes = []
        self.equipment_pvp = []
        self.training = []
