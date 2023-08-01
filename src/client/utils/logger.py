from functools import partial
import colorama


def log(code: str, color: str, message: str):
    """
    Outputs a message with the specified color and code.

    Parameters:
    code (str): The code of the message (for example, "info" or "error").
    color (str): The color of the message (for example, colorama.Fore.RED).
    message (str): The text of the message.

    Functionality:
    Formats the message as "[CODE] Message" and outputs it with the specified color.
    """
    print(f"{color}[{code.upper()}] {message}")


def error(message: str):
    """
    Outputs an error message in red color.

    Parameters:
    message (str): The text of the error message.

    Functionality:
    Calls log() with the code "error" and a red color (colorama.Fore.RED) to output an
    error message.
    """

    log(color=colorama.Fore.RED, code="error", message=message)


def info(message: str):
    """
    Outputs an informational message in green color.

    Parameters:
    message (str): The text of the informational message.

    Functionality:
    Calls log() with the code "info" and a green color (colorama.Fore.GREEN) to output an
    information message.
    """
    log(color=colorama.Fore.GREEN, code="info", message=message)
