from utils import models, classes, helper
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

app = FastAPI()
users = list()
events = dict()
tokens: dict[str, classes.User] = dict()


@app.get("/events")
def get_events(json_row: models.Token):
    """
    Returns a list of events for the user.

    Parameters:
    json_row (models.Token): The model of the access token.

    Functionality:
    Retrieves an access token from json_row.
    Tries to retrieve a list of events for the user by token from events.
    If the event list is found, clears it and returns it in the response.
    If the event list is not found by token, returns a response with status 401.
    """

    token: str = jsonable_encoder(json_row)["token"]
    print(events[token])

    try:
        answer = list(map(lambda x: x.to_json(), events[token]))
        events[token].clear()
    except KeyError:
        return Response(status_code=401)

    return JSONResponse(content={"events": answer})


@app.get("/users")
def get_users():
    """
    Returns a list of users.

    Parameters:
    No

    Functionality:
    Serializes all users into JSON using their to_json() method.
    Returns a list of serialized users in the response.
    """

    return JSONResponse(content={"users": list(map(lambda x: x.to_json(), users))})


@app.get("/isvalid")
def isvalid():
    """
    Checks the availability of the server.

    Parameters:
    No

    Functionality:
    Returns a response with status 200 and JSON {"valid": True} to verify server availability.
    """

    return JSONResponse(content={"valid": True})


@app.post("/join")
def join(json_row: models.JoinInfo):
    """
    Adds a user.

    Parameters:
    json_row (models.JoinInfo): Model with the user's join information.

    Functionality:
    Extracts user data from json_row.
    Creates an instance of the user.
    If the user has not yet been added, adds it to the user list and token dictionary, returns status 201.
    If the user has already been added, returns its token and status 200.
    Creates an empty event list for the user.
    Adds a "join" event for the user.
    Returns the user's token in the response.
    """

    print(users)
    json_data: dict = jsonable_encoder(json_row)

    user = classes.User(json_data["id"], json_data["username"])

    if user not in users:
        status_code = 201
        users.append(user)
        tokens[user.token] = user
    else:
        status_code = 200
        for user in users:
            if user.id == json_data["id"]:
                break

    events[user.token] = list()

    helper.add_events(events, "join", json_data)

    return JSONResponse(content={"token": user.token}, status_code=status_code)


@app.post("/message")
def send_message(json_row: models.Message):
    """
    Sends a message.

    Parameters:
    json_row (models.Message): The model of the message.

    Functionality:
    Retrieves message data from json_row.
    Tries to retrieve data about the user who sent the message from tokens by token.
    If the user is found, adds a "message" event with the message and user data.
    If the user is not found by token, returns a response with status 401.
    Returns a response with status 201 if successful.
    """

    json_data = jsonable_encoder(json_row)
    username = tokens[json_data["token"]].to_json().get("username")

    try:
        helper.add_events(events, "message", dict(username=username, **json_data))
    except KeyError:
        return Response(status_code=401)

    return Response(status_code=201)
