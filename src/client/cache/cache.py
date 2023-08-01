import os


def write_to_cache(id: str, data: str):
    """
    Writes data to the cache by identifier.

    Parameters:
    id (str): The identifier of the entry in the cache.
    data (str): The data to write to the cache.
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
    Retrieves data from cache by identifier.

    Parameters:
    id (str): The identifier of the entry in the cache.

    Functionality:
    Tries to open a file named {id}.data and read it.
    If the file is found, the data is decoded from bytes to a string and returned.
    If the file is not found, None is returned.
    """
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        return ""

    file_path = os.path.join(cache_dir, f"{id}.data")

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
