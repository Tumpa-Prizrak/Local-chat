from utils import classes


def add_events(events: dict, event: str, json_data: dict):
    """
    Добавляет событие в список событий.

    Параметры:
    events (dict): Словарь событий, ключ - токен пользователя, значение - список событий.
    event (str): Тип добавляемого события (join, message и т.д.).
    json_data (dict): Данные о событии.

    Функциональность:
    Удаляет поле "token" из json_data, если оно присутствует.
    Добавляет новое событие типа event в список событий для каждого пользователя в events.
    """

    if "token" in json_data:
        del json_data["token"]
    for event in events:
        events[event].append(classes.Event(event=event, **json_data))
