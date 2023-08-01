from pydantic import BaseModel


class Snowflake(BaseModel):
    """
    The Snowflake class is a base model with an ID and a timestamp.

    Parameters:
    id (int): Unique ID.
    timestamp (int): The timestamp in seconds.

    Functionality:
    Defines the basic model structure with ID and timestamp.
    """

    id: int
    timestamp: int


class JoinInfo(Snowflake):
    """
    The JoinInfo class is a model for passing information about a user's connection.

    Parameters:
    username (str): The username of the user.

    Functionality:
    Inherited from Snowflake.
    Adds a username field to store the username.
    """

    username: str


class Token(BaseModel):
    """
    Token class - a model for passing an access token.

    Parameters:
    token (str): The access token.

    Functionality:
    Defines the structure of the model for passing an access token.
    """

    token: str


class Message(Token, Snowflake):
    """
    The Message class is a model for sending a message.

    Parameters:
    message (str): The text of the message.

    Functionality:
    Inherited from Token and Snowflake.
    Adds a message field to store the message text.
    """

    message: str
