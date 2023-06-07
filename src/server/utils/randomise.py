import random
import string

valid = string.ascii_letters + string.digits


def generate_token(lenth: int = 5) -> str:
    """
    Генерирует случайный токен доступа.
    
    Параметры:
    lenth (int): Длина генерируемого токена. По умолчанию равна 5.
    
    Функциональность:
    Генерирует случайную строку символов длиной lenth из букв латинского алфавита и цифр.
    Возвращает сгенерированный токен.
    """
    
    return "".join(random.choices(valid, k=lenth))
