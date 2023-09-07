import colorama as c
import datetime


class ColoredText:
    text: str
    color: c.Fore

    def __init__(self, *, text: str, color: c.Fore = c.Fore.WHITE):
        self.text = text
        self.color = color

    def __str__(self):
        return f"{self.color}{self.text}{c.Fore.RESET}"


def _log(*, level: ColoredText, msg: ColoredText):
    print(f"{level}: {msg}")
    with open(f"logs/{datetime.datetime.now().strftime('')}", "a") as f:
        f.write(f"{level.text}: {msg.text}\n")


def error(msg: str): _log(
    level=ColoredText(text="[ERROR]", color=c.Fore.RED),
    msg=ColoredText(text=msg)
)


def warning(msg: str): _log(
    level=ColoredText(text="[WARNING]", color=c.Fore.YELLOW),
    msg=ColoredText(text=msg)
)


def info(msg: str): _log(
    level=ColoredText(text="[INFO]", color=c.Fore.BLUE),
    msg=ColoredText(text=msg)
)


def log(msg: str): _log(
    level=ColoredText(text="[LOG]", color=c.Fore.WHITE),
    msg=ColoredText(text=msg)
)


def debug(msg: str): _log(
    level=ColoredText(text="[DEBUG]", color=c.Fore.GREEN),
    msg=ColoredText(text=msg)
)
