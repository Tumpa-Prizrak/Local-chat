def to_cache(id: str, data: str):
    """
    Записывает данные в кэш по идентификатору.

    Параметры: 
    id (str): Идентификатор записи в кэше.
    data (str): Данные для записи в кэш.
    """
    with open(f"cache\\{id}.cac", "wb") as f:
        f.write(data.encode("utf-8"))


def from_cache(id: str):
    """
    Извлекает данные из кэша по идентификатору.
    
    Параметры:
    id (str): Идентификатор записи в кэше.
    
    Функциональность:
    Пытается открыть файл с именем {id}.cac и прочитать его. 
    Если файл найден, данные декодируются из байтов в строку и возвращаются.
    Если файл не найден, возвращается None.
    """
    try:
        with open(f"cache\\{id}.cac", "rb") as f:
            return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
