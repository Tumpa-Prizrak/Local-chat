from contextlib import suppress
import requests as r
from utils import networking
import colorama
from cache import cache
from utils import utils
import sys
from utils import logger
import threading
from time import sleep

colorama.init(autoreset=True)

base = None
token = None
userid = networking.get_my_ip().split(".")[-1]
threads_active = True


if (username := cache.read_from_cache("username")) is None:
    username = input(f"{colorama.Fore.YELLOW}Enter your username: ")
    cache.write_to_cache("username", username)
    utils.clear_console()


@utils.count
def connect():
    """
    Подключается к серверу.

    Параметры:
    Нет

    Функциональность:
    Сканирует сеть в поисках сервера.
    Если сервер не найден, выводит сообщение об ошибке и завершает работу.
    Если сервер найден, сохраняет его IP-адрес в глобальной переменной base.
    """

    global base
    logger.info("Connecting to server...")
    if (base := networking.find_server(networking.scan())) is None:
        logger.error("Server is not found. Try again later")
        input()
        sys.exit(1)
    else:
        base = f"http://{base}"


logger.info(f"Done in {connect()} seconds...")


@utils.count
def join():
    global token
    """
    Присоединяется к серверу.

    Параметры:
    Нет

    Функциональность:
    Делает POST-запрос к /join на сервере с указанием id, username и timestamp.
    Получает токен доступа к серверу из ответа.
    Если произошла ошибка TimeoutError, выводит сообщение об ошибке и завершает работу.
    """

    logger.info("Joining...")
    try:
        request = r.post(
            f"{base}/join",
            json={"id": userid, "timestamp": utils.timestamp(), "username": username},
        )
        token = request.json()["token"]
    except TimeoutError:
        logger.error("Coudn't connect to server. Exiting...")
        input()
        sys.exit(1)


logger.info(f"Joined in {join()} seconds...")


def users():
    """
    Выводит список подключенных пользователей.

    Параметры:
    Нет

    Функциональность:
    Делает GET-запрос к /users на сервере.
    Получает список подключенных пользователей в ответе.
    Выводит имя пользователя и id для каждого подключенного пользователя.
    """

    request = r.get(f"{base}/users")
    print("Loggined users:")
    for user in request.json()["users"]:
        print(f"{user['username']} (id: {user['id']})")
users()


def send_message():
    while threads_active:
        with suppress(EOFError):
            if line := input():
                r.post(f"{base}/message", json={
                    "id": userid,
                    "timestamp": utils.timestamp(),
                    "token": token,
                    "message": line
                })


def get_events():
    global threads_active
    while threads_active:
        spis = r.get(f"{base}/events", json={
            "token": token
        }).json().get("events")

        for event in spis:
            utils.print_event(event)
        sleep(5)

send_message_thread = threading.Thread(target=send_message)
get_events_thread = threading.Thread(target=get_events)
send_message_thread.start()
get_events_thread.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    threads_active = False
    with suppress(EOFError):
        send_message_thread.join()
    with suppress(EOFError):
        get_events_thread.join()
    logger.info("Successfully exited")
