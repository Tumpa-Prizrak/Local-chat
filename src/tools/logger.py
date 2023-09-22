import colorama as c
import datetime


class ColoredText:
    """
    A class to represent colored text.

    Attributes:

    text (str): The text content.
    color (Fore): The colorama Fore color for the text.

    Methods:

    __init__(text, color=Fore.WHITE):
    Constructor to initialize the text and color attributes.

    __str__():
    Returns the colored text by applying colorama formatting.
    """

    text: str
    color: c.Fore

    def __init__(self, *, text: str, color: c.Fore = c.Fore.WHITE):
        """
        Initialize the colored text.

        Parameters:
        text (str): The text content
        color (Fore): The colorama Fore color
        """
        self.text = text
        self.color = color

    def __str__(self):
        """
        Return the colored text string.

        Applies the colorama formatting to the text.
        """
        return f"{self.color}{self.text}{c.Fore.RESET}"


class Log:
    """
    Log functions for different log levels.

    Each function accepts a message string and calls the _log() function
    to log it with the appropriate log level and color.

    Parameters:
    msg (str): The message to log.

    Functions:

    error(msg): Log an error message in red.

    warning(msg): Log a warning message in yellow.

    info(msg): Log an informational message in blue.

    log(msg): Log a generic message in white.

    debug(msg): Log a debug message in green.

    The _log() function handles printing to console and file.
    """

    @staticmethod
    def _log(*, level: ColoredText, msg: ColoredText):
        """
        Log a message to console and file.

        Parameters:
        level (ColoredText): The log level (INFO, WARNING, etc.)
        msg (ColoredText): The message text

        Functionality:
        1. Print the log message to console formatted as:
           "{level}: {msg}"
        2. Open a log file named with the current timestamp
        3. Write the log message to the file as:
           "{level.text}: {msg.text}"
        """
        print(f"{level}: {msg}")
        with open(f"logs/{datetime.datetime.now().strftime('')}", "a") as f:
            f.write(f"{level.text}: {msg.text}\n")

    @staticmethod
    def error(msg: str):
        Log._log(
            level=ColoredText(text="[ERROR]", color=c.Fore.RED),
            msg=ColoredText(text=msg),
        )

    @staticmethod
    def warning(msg: str):
        Log._log(
            level=ColoredText(text="[WARNING]", color=c.Fore.YELLOW),
            msg=ColoredText(text=msg),
        )

    @staticmethod
    def info(msg: str):
        Log._log(
            level=ColoredText(text="[INFO]", color=c.Fore.BLUE),
            msg=ColoredText(text=msg),
        )

    @staticmethod
    def log(msg: str):
        Log._log(
            level=ColoredText(text="[LOG]", color=c.Fore.WHITE),
            msg=ColoredText(text=msg),
        )

    @staticmethod
    def debug(msg: str):
        Log._log(
            level=ColoredText(text="[DEBUG]", color=c.Fore.GREEN),
            msg=ColoredText(text=msg),
        )
