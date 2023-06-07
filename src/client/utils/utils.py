from os import system
import datetime
import time


def clear_console():
    """
    Очищает консоль.

    Параметры:
    Нет

    Функциональность:
    Пытается очистить консоль командой "cls" для Windows.
    Если команда "cls" не сработала (вернула код отличный от 0),
    выполняет очистку консоли командой "clear" для Linux/Mac.
    """
    if system("cls") != 0:
        system("clear")


def count(func):
    """
    Декоратор для подсчета времени выполнения функции.

    Параметры:
    func (function): Декорируемая функция.

    Функциональность:
    Запоминает время начала выполнения функции.
    Вызывает декорируемую функцию.
    Вычисляет разницу между временем окончания и начала выполнения.
    Возвращает это время.
    """

    def wrapper():
        now = time.perf_counter()
        func()
        return time.perf_counter() - now

    return wrapper


def timestamp(time: datetime.datetime = None) -> int:
    """
    Получает timestamp (количество секунд с начала эпохи) для указанной даты и времени.

    Параметры:
    time (datetime.datetime): Дата и время для получения timestamp. По умолчанию берется текущая дата и время.

    Функциональность:
    Если параметр time не указан, берет текущую дату и время.
    Получает timestamp для указанной даты и времени с помощью метода .mktime().
    Возвращает полученный timestamp.
    """

    if time is None:
        time = datetime.datetime.now()

    return time.mktime(time.timetuple())
