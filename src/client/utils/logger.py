from functools import partial
import colorama


def log(code: str, color: str, message: str):
    print(f"{color}[{code.upper()}] {message}")


def error(message: str):
    log(color=colorama.Fore.RED, code="error", message=message)


def info(message: str):
    log(color=colorama.Fore.GREEN, code="info", message=message)
