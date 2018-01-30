from abc import ABCMeta, abstractmethod
from enum import Enum

class LoadableTypeEnum(Enum):
    Achievement = "Achievement"
    Character = "Character"
    Guild = "Guild"
    GuildUpgrade = "GuildUpgrade"
    Item = "Item"
    ItemStat = "ItemStat"
    Mastery = "Mastery"
    MiniPet = "MiniPet"
    Skill = "Skill"
    Skin = "Skin"
    Title = "Title"

class LoadableObjectVisitorBase(object, metaclass=ABCMeta):

    @abstractmethod
    def collect(self, obj):
        raise NotImplementedError()

class LoadableObjectBase(object, metaclass=ABCMeta):
    """Base class for all GW2 API objects that can be retreived from API"""

    @abstractmethod
    def _populate_inner(self, json):
        raise NotImplementedError()

    def populate(self, json):
        self._populate_inner(json)


class LoadableObjectContainer():
    """Container for GW2 API object pending loading"""

    _visitors = []
    def register_visitor(visitor: LoadableObjectVisitorBase):
        LoadableObjectContainer._visitors.append(visitor)

    def __init__(self, id, type: LoadableTypeEnum):
        self.id = id
        self.loadable_type = type
        self.object = None

        for visitor in LoadableObjectContainer._visitors:
            visitor.collect(self)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, value: LoadableObjectBase):
        self._object = value

    @property
    def has_loaded(self):
        return self.object != None

class LoadableObjectVisitorBase(object, metaclass=ABCMeta):

    @abstractmethod
    def collect(self, obj: LoadableObjectContainer):
        raise NotImplementedError()
