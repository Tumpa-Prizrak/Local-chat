import randomise


class User:
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username
        self.token = randomise.generate_token()
