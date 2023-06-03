from src.utils import randomise
from abc import ABC, abstractmethod


class JsonSerializable(ABC):
    @classmethod
    def from_json(cls, data: dict, /):
        return cls(**data)

    @abstractmethod
    def to_json(self):
        ...


class User(JsonSerializable):
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username
        self.token = randomise.generate_token()

    def to_json(self, safe: bool = True):
        d = {
            "id": self.id,
            "username": self.username,
        }
        if not safe:
            d["token"] = self.token

        return d

    def __eq__(self, value: object) -> bool:
        print("__eq__")
        return self.id == value.id if isinstance(value, User) else False
class Event(JsonSerializable):
    def __init__(self, event: str, id: int, timestamp: int, **kwargs):
        self.event = event
        self.id = id
        self._timestamp = timestamp
        self.info = kwargs

    def to_json(self):
        return dict(
            event=self.event, id=self.id, timestamp=self._timestamp, **self.info
        )
