import requests as r
from utils import networking
import colorama
from cache import cache
from utils import utils
import sys
import select
from utils import logger
import asyncio

colorama.init(autoreset=True)

base = None
token = None
userid = networking.get_my_ip().split(".")[0]

if (username := cache.from_cache("username")) is None:
    username = input(f"{colorama.Fore.YELLOW}Enter your username: ")
    cache.to_cache("username", username)
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


logger.info(f"Done in {connect()} seconds...")


@utils.count
def join():
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


async def get_events():
    pass


def send_message(message: str):
    pass


loop = asyncio.get_event_loop()
loop.create_task(get_events())
loop.run_forever()
while True:
    ready, _, _ = select.select([sys.stdin], [], [], 1)
    if not ready:
        continue
    if message := sys.stdin.readline().rstrip("\n"):
        send_message(message)
