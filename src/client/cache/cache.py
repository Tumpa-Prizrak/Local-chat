import os


def write_to_cache(id: str, data: str):
    """
    Записывает данные в кэш по идентификатору.

    Параметры:
    id (str): Идентификатор записи в кэше.
    data (str): Данные для записи в кэш.
    """
    if not isinstance(id, str) or not isinstance(data, str):
        raise TypeError("Аргументы должны быть строками!")

    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    file_path = os.path.join(cache_dir, f"{id}.cac")

    try:
        with open(file_path, "wb") as f:
            f.write(data.encode("utf-8"))
    except (FileNotFoundError, PermissionError) as err:
        print(f"Ошибка при записи в кэш: {err}")


def read_from_cache(id: str):
    """
    Извлекает данные из кэша по идентификатору.

    Параметры:
    id (str): Идентификатор записи в кэше.

    Функциональность:
    Пытается открыть файл с именем {id}.cac и прочитать его.
    Если файл найден, данные декодируются из байтов в строку и возвращаются.
    Если файл не найден, возвращается None.
    """
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        return ""

    file_path = os.path.join(cache_dir, f"{id}.cac")

    try:
        with open(file_path, "rb") as f:
            encoding = "utf-8"
            try:
                return f.read().decode(encoding)
            except UnicodeDecodeError:
                encoding = "cp1251"
                return f.read().decode(encoding)
    except FileNotFoundError:
        return ""
