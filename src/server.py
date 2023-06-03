import bottle
from utils.classes import User

users = list()
events = dict()


@bottle.post("/join")
def join():
    json_data = bottle.request.json
    user = User(json_data["id"], json_data["username"])
    users.append(user)
    events[user.token] = []


@bottle.get("/events")
def events():
    pass


bottle.run(host="0.0.0.0", port=48658)
