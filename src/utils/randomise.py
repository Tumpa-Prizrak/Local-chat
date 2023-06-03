import random
import string

valid = string.ascii_letters + string.digits


def generate_token(lenth: int = 5) -> str:
    return "".join(random.choices(valid, k=lenth))
