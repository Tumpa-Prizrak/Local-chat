from functools import partial
import colorama


def log(code: str, color: str, message: str):
    """
    Выводит сообщение с указанным цветом и кодом.

    Параметры:
    code (str): Код сообщения (например, "info" или "error").
    color (str): Цвет сообщения (например, colorama.Fore.RED).
    message (str): Текст сообщения.

    Функциональность: 
    Форматирует сообщение в виде "[КОД] Сообщение" и выводит его с указанным цветом.
    """
    print(f"{color}[{code.upper()}] {message}")


def error(message: str):
    """
    Выводит сообщение об ошибке красным цветом.

    Параметры:
    message (str): Текст сообщения об ошибке.

    Функциональность:
    Вызывает log() с кодом "error" и красным цветом (colorama.Fore.RED) для вывода 
    сообщения об ошибке.
    """

    log(color=colorama.Fore.RED, code="error", message=message)


def info(message: str):
    """
    Выводит информационное сообщение зеленым цветом.
    
    Параметры:
    message (str): Текст информационного сообщения.
    
    Функциональность:
    Вызывает log() с кодом "info" и зеленым цветом (colorama.Fore.GREEN) для вывода 
    информационного сообщения.
    """
    log(color=colorama.Fore.GREEN, code="info", message=message)
