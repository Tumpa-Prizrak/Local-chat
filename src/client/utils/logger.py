from functools import partial
import colorama

def log(code: str, color: str, message: str):
    print(f"{color}[{code.upper()}] {message}")

error = partial(log, color=colorama.Fore.RED, code="error")
info = partial(log, color=colorama.Fore.GREEN, code="info")
