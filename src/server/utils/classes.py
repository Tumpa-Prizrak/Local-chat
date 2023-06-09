from utils import randomise
from abc import ABC, abstractmethod


class JsonSerializable(ABC):
    """
    Абстрактный класс для сериализации в JSON.

    Параметры:
    Нет

    Функциональность:
    Определяет абстрактный метод to_json() для сериализации в JSON.
    Определяет классовый метод from_json() для десериализации из JSON.
    """

    @classmethod
    def from_json(cls, data: dict, /):
        return cls(**data)

    @abstractmethod
    def to_json(self):
        ...


class User(JsonSerializable):
    """
    Класс пользователя.

    Параметры:
    id (int): ID пользователя.
    username (str): Имя пользователя.

    Функциональность:
    Создает экземпляр пользователя с указанным ID и именем.
    Генерирует уникальный токен доступа для пользователя.
    Определяет метод to_json() для сериализации в JSON. По умолчанию не включает токен в JSON, но может включить его при safe=False.
    Определяет метод __eq__() для сравнения экземпляров пользователя. Сравнивает по ID.
    """

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
    """
    Класс события.

    Параметры:
    event (str): Тип события (join, message и т.д.).
    id (int): ID пользователя, совершившего событие.
    timestamp (int): Временная метка события.
    **kwargs: Дополнительная информация о событии.

    Функциональность:
    Создает экземпляр события с указанными параметрами.
    Определяет метод to_json() для сериализации в JSON. Включает в JSON тип события, ID пользователя, временную метку и дополнительную информацию.
    """

    def __init__(self, event: str, id: int, timestamp: int, **kwargs):
        self.event = event
        self.id = id
        self._timestamp = timestamp
        self.info = kwargs

    def to_json(self):
        return dict(
            event=self.event, id=self.id, timestamp=self._timestamp, **self.info
        )
