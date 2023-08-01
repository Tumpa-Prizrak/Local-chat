from os import system
import datetime
import time
from utils import logger


def clear_console():
    """
    Clears the console.

    Parameters:
    No

    Functionality:
    Attempts to clear the console with the "cls" command for Windows.
    If the "cls" command fails (returns a code other than 0),
    clears the console with the "clear" command for Linux/Mac.
    """
    if system("cls") != 0:
        system("clear")


def count(func):
    """
    A decorator for counting the execution time of a function.

    Functionality:
    Remembers the start time of the function execution.
    Calls the function.
    Calculates the difference between the end time and the start time of execution.
    Returns this time.
    """

    def wrapper():
        now = time.perf_counter()
        func()
        return time.perf_counter() - now

    return wrapper


def timestamp(dt: datetime.datetime | None = None) -> int:
    """
    Gets the timestamp (number of seconds since the beginning of the epoch) for the specified date and time.

    Parameters:
    time (datetime.datetime): The date and time to get the timestamp. The default is to take the current date and time.

    Functionality:
    If no time parameter is specified, takes the current date and time.
    Gets the timestamp for the specified date and time using the .mktime() method.
    Returns the obtained timestamp.
    """

    if dt is None:
        dt = datetime.datetime.now()

    return time.mktime(dt.timetuple())  # type: ignore


def from_timestamp(timestamp: int) -> str:
    """
    Converts timestamp (in seconds) to date and time.

    Parameters:
    timestamp (int): The time in seconds.

    Returns:
    str: Date and time in HH:MM format.
    """
    from datetime import datetime

    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%H:%M")


def print_event(event: dict) -> None:
    """
    Print an event dictionary in a human-readable format.
    """
    match (event.get("event")):
        case "join":
            logger.info(
                f"[{from_timestamp(event.get('timestamp'))}] User {event.get('username')} (ID: {event.get('id')}) joined"
            )
        case "message":
            print(
                f"[{from_timestamp(event.get('timestamp'))}] {event.get('username')}: {event.get('message')}"
            )
        case _:
            logger.error(f"Event {event.get('event')} is unknown")
