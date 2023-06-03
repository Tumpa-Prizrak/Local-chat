from src.utils import classes

def add_events(events: dict, event: str, json_data: dict):
    for event in events:
        events[event] = classes.Event(event=event, **json_data)
