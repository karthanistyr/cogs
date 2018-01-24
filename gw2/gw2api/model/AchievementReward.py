from enum import Enum
from gw2api.model.LoadableObject import LoadableObjectContainer, LoadableTypeEnum

class RewardType(Enum):
    Coins = "Coins"
    Item = "Item"
    Title = "Title"
    Mastery = "Mastery"

class AchievementReward:
    def __init__(self, type: RewardType):
        self.type = type

class AchievementRewardCoins(AchievementReward):
    def __init__(self, json=None):
        super().__init__(RewardType.Coins)
        self.count = None

        if(json is not None):
            self.load_from_json(json)

    def load_from_json(self, json):
        self.count = json.get("count", None)

class AchievementRewardItem(AchievementReward):
    def __init__(self, json=None):
        super().__init__(RewardType.Item)
        self.count = None
        self.item = None

        if(json is not None):
            self.load_from_json(json)

    def load_from_json(self, json):
        self.count = json.get("count", None)
        self.item = LoadableObjectContainer(json["id"], LoadableTypeEnum.Item)

class AchievementRewardTitle(AchievementReward):
    def __init__(self, json=None):
        super().__init__(RewardType.Title)
        self.title = None

        if(json is not None):
            self.load_from_json(json)

    def load_from_json(self, json):
        self.count = json.get("count", None)
        self.title = LoadableObjectContainer(json["id"], LoadableTypeEnum.Title)

class AchievementRewardMastery(AchievementReward):
    def __init__(self, json=None):
        super().__init__(RewardType.Mastery)
        self.region = None
        self.mastery = None

        if(json is not None):
            self.load_from_json(json)

    def load_from_json(self, json):
        self.region = json["region"]
        self.mastery = LoadableObjectContainer(json["id"], LoadableTypeEnum.Mastery)
