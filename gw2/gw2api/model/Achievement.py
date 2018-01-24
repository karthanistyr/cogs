from enum import Enum
from gw2api.model.LoadableObject import LoadableObjectBase, LoadableTypeEnum
from gw2api.model.AchievementReward import *

class AchievementTypeEnum(Enum):
    Default = "Default"
    ItemSet = "ItemSet"

class AchievementFlagEnum(Enum):
    Permanent = "Permanent"
    Daily = "Daily"
    Weekly = "Weekly"
    Monthly = "Monthly"
    Pvp = "Pvp"
    MoveToTop = "MoveToTop"
    CategoryDisplay = "CategoryDisplay"
    IgnoreNearlyComplete = "IgnoreNearlyComplete"
    Repeatable = "Repeatable"
    Hidden = "Hidden"
    RequiresUnlock = "RequiresUnlock"
    RepairOnLogin = "RepairOnLogin"

class AchievementTier:
    def __init__(self, json=None):
        self.count = None
        self.points = None

        if(json is not None):
            self.load_from_json(json)

    def load_from_json(self, json: dict):
        self.count = json.get("count", None)
        self.points = json.get("points", None)

class Achievement(LoadableObjectBase):
    def __init__(self, id):
        self.id = id
        self.name = None
        self.description = None
        self.requirement = None
        self.locked_text = None
        self.type = None
        self.flags = []
        self.tiers = []
        self.prerequisites = []
        self.rewards = []
        self.bits = []
        self.point_cap = None

    def _populate_inner(self, json):
        self.name = json.get("name", None)
        self.description = json.get("description", None)
        self.requirement = json.get("requirement", None)
        self.locked_text = json.get("locked_text", None)
        self.type = json.get("type", None)

        for flag_data in json["flags"]:
            self.flags.append(flag_data)

        for tier_data in json["tiers"]:
            self.tiers.append(AchievementTier(tier_data))

        if("prerequisites" in json):
            for prereq_data in json["prerequisites"]:
                self.prerequisites.append(LoadableObjectContainer(prereq_data, LoadableTypeEnum.Achievement))

        if("rewards" in json):
            for reward in json["rewards"]:
                if(reward["type"] == RewardType.Coins.value):
                    self.rewards.append(AchievementRewardCoins(reward))
                if(reward["type"] == RewardType.Item.value):
                    self.rewards.append(AchievementRewardItem(reward))
                if(reward["type"] == RewardType.Title.value):
                    self.rewards.append(AchievementRewardTitle(reward))
                if(reward["type"] == RewardType.Mastery.value):
                    self.rewards.append(AchievementRewardMastery(reward))
