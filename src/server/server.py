from utils import models, classes, utils
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

app = FastAPI()
users = list()
events = dict()
tokens: dict[classes.User] = dict()


@app.get("/events")
def get_events(json_row: models.Token):
    """
    Возвращает список событий для пользователя.

    Параметры:
    json_row (models.Token): Модель токена доступа.

    Функциональность:
    Извлекает токен доступа из json_row.
    Пытается получить список событий для пользователя по токену из events.
    Если список событий найден, очищает его и возвращает в ответе.
    Если список событий не найден по токену, возвращает ответ со статусом 401.
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
    Возвращает список пользователей.

    Параметры:
    Нет

    Функциональность:
    Сериализует всех пользователей в JSON с помощью их метода to_json().
    Возвращает список сериализованных пользователей в ответе.
    """

    return JSONResponse(content={"users": list(map(lambda x: x.to_json(), users))})


@app.get("/isvalid")
def get_users():
    """
    Проверяет доступность сервера.

    Параметры:
    Нет

    Функциональность:
    Возвращает ответ со статусом 200 и JSON {"valid": True} для проверки доступности сервера.
    """

    return JSONResponse(content={"valid": True})


@app.post("/join")
def join(json_row: models.JoinInfo):
    """
    Добавляет пользователя.

    Параметры:
    json_row (models.JoinInfo): Модель с информацией о подключении пользователя.

    Функциональность:
    Извлекает данные о пользователе из json_row.
    Создает экземпляр пользователя.
    Если пользователь еще не добавлен, добавляет его в список пользователей и словарь токенов, возвращает статус 201.
    Если пользователь уже добавлен, возвращает его токен и статус 200.
    Создает пустой список событий для пользователя.
    Добавляет событие "join" для пользователя.
    Возвращает токен пользователя в ответе.
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

    utils.add_events(events, "join", json_data)

    return JSONResponse(content={"token": user.token}, status_code=status_code)


@app.post("/message")
def send_message(json_row: models.Message):
    """
    Отправляет сообщение.

    Параметры:
    json_row (models.Message): Модель сообщения.

    Функциональность:
    Извлекает данные о сообщении из json_row.
    Пытается получить данные о пользователе, отправившем сообщение, из tokens по токену.
    Если пользователь найден, добавляет событие "message" с данными о сообщении и пользователе.
    Если пользователь не найден по токену, возвращает ответ со статусом 401.
    Возвращает ответ со статусом 201 в случае успеха.
    """

    json_data = jsonable_encoder(json_row)
    username = tokens[json_data["token"]].to_json().get('username')

    try:
        utils.add_events(
            events, "message", dict(
                username=username,
                **json_data
            )
        )
    except KeyError:
        return Response(status_code=401)

    return Response(status_code=201)
