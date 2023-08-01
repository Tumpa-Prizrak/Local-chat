from utils import randomise
from abc import ABC, abstractmethod


class JsonSerializable(ABC):
    """
    An abstract class for serialization to JSON.

    Parameters:
    No

    Functionality:
    Defines an abstract method to_json() for serialization to JSON.
    Defines a class method from_json() for deserialization from JSON.
    """

    @classmethod
    def from_json(cls, data: dict, /):
        return cls(**data)

    @abstractmethod
    def to_json(self):
        ...


class User(JsonSerializable):
    """
    User Class.

    Parameters:
    id (int): user ID.
    username (str): The username of the user.

    Functionality:
    Creates a user instance with the specified user ID and username.
    Generates a unique access token for the user.
    Defines a to_json() method for serialization to JSON. By default, does not include the token in JSON, but can include it when safe=False.
    Defines the __eq__() method to compare user instances. Compares by ID.
    """

    def __init__(self, userid: int, username: str):
        self.id = userid
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
    """
    Event Class.

    Parameters:
    event (str): Type of event (join, message, etc.).
    id (int): ID of the user who committed the event.
    timestamp (int): The timestamp of the event.
    **kwargs: Additional information about the event.

    Functionality:
    Creates an event instance with the specified parameters.
    Defines the to_json() method for serialization to JSON. Includes the event type, user ID, timestamp, and additional information in JSON.
    """

    def __init__(self, event: str, event_id: int, timestamp: int, **kwargs):
        self.event = event
        self.id = event_id
        self._timestamp = timestamp
        self.info = kwargs

    def to_json(self):
        return dict(
            event=self.event, id=self.id, timestamp=self._timestamp, **self.info
        )
