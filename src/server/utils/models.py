from pydantic import BaseModel


class Snowflake(BaseModel):
    id: int
    timestamp: int


class JoinInfo(Snowflake):
    username: str


class Token(BaseModel):
    token: str


class Message(Token, Snowflake):
    message: str
