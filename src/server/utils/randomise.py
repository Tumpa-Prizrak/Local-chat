import random
import string

valid = string.ascii_letters + string.digits


def generate_token(length: int = 5) -> str:
    """
    Generates a random access token.

    Parameters:
    length (int): The length of the token to be generated. Defaults to 5.

    Functionality:
    Generates a random character string of length from Latin alphabet letters and numbers.
    Returns the generated token.
    """

    return "".join(random.choices(valid, k=length))
