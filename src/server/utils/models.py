from pydantic import BaseModel


class Snowflake(BaseModel):
    """
    Класс Snowflake - базовая модель с ID и временной меткой.
    
    Параметры:
    id (int): Уникальный ID.
    timestamp (int): Временная метка в секундах.
    
    Функциональность: 
    Определяет базовую структуру модели с ID и временной меткой.
    """
    
    id: int
    timestamp: int


class JoinInfo(Snowflake):
    """
    Класс JoinInfo - модель для передачи информации о подключении пользователя.
    
    Параметры:
    username (str): Имя пользователя.
    
    Функциональность:
    Наследуется от Snowflake.
    Добавляет поле username для хранения имени пользователя.
    """
    
    username: str


class Token(BaseModel):
    """
    Класс Token - модель для передачи токена доступа.
    
    Параметры:
    token (str): Токен доступа.
    
    Функциональность:
    Определяет структуру модели для передачи токена доступа.
    """
    
    token: str


class Message(Token, Snowflake):
    """
    Класс Message - модель для передачи сообщения.
    
    Параметры:
    message (str): Текст сообщения.
    
    Функциональность:
    Наследуется от Token и Snowflake.
    Добавляет поле message для хранения текста сообщения.
    """
    
    message: str
