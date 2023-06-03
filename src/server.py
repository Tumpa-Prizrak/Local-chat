from src.utils import models, classes, utils
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

app = FastAPI()
users = list()
events = dict()

@app.post("/join")
def join(json_row: models.JoinInfo):
    print(users)
    json_data: dict = jsonable_encoder(json_row)

    user = classes.User(json_data["id"], json_data["username"])

    if user not in users:
        status_code = 201
        users.append(user)
    else:
        status_code = 200
        for user in users:
            if user.id == json_data["id"]:
                break

    events[user.token] = list()
    
    return JSONResponse(content={
        "token": user.token
    }, status_code=status_code)

@app.get("/events")
def get_events(json_row: models.Token):
    token: str = jsonable_encoder(json_row)["token"]
    
    try:
        answer = list(map(lambda x: x.to_json(), events[token]))
        events[token].clear()
    except KeyError:
        return Response(status_code=401)
    
    return JSONResponse(content={
        "events": answer
    })

@app.post("/message")
def send_message(json_row: models.Message):
    json_data = jsonable_encoder(json_row)

    utils.add_events(events, "message", json_data)

    return Response(status_code=201)
