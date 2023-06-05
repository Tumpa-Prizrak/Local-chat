def to_cache(id: str, data: str):
    with open(f"cache\\{id}.cac", "wb") as f:
        f.write(data.encode("utf-8"))


def from_cache(id: str):
    try:
        with open(f"cache\\{id}.cac", "rb") as f:
            return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
