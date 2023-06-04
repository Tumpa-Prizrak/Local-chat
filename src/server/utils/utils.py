from utils import classes


def add_events(events: dict, event: str, json_data: dict):
    if "token" in json_data:
        del json_data["token"]
    for event in events:
        events[event].append(classes.Event(event=event, **json_data))
