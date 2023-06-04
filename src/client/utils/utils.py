from os import system
import datetime
import time


def clear_console():
    if system("cls") != 0:
        system("clear")


def count(func):
    def wrapper():
        now = time.perf_counter()
        func()
        return time.perf_counter() - now

    return wrapper


def timestamp(time: datetime.datetime = None) -> int:
    if time is None:
        time = datetime.datetime.now()

    return time.mktime(time.timetuple())
