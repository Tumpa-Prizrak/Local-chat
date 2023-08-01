from utils import classes


def add_events(events: dict, event: str, json_data: dict):
    """
    Adds an event to the event list.

    Parameters:
    events (dict): Dictionary of events, key is the user token, value is the list of events.
    event (str): The type of event to add (join, message, etc.).
    json_data (dict): Data about the event.

    Functionality:
    Removes the "token" field from json_data, if present.
    Adds a new event of type event to the event list for each user in events.
    """

    if "token" in json_data:
        del json_data["token"]
    for value in events.values():
        value.append(classes.Event(event=event, **json_data))
