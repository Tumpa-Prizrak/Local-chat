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


@utils.count
def connect():
    """
    Connects to the server.

    Parameters:
    No

    Functionality:
    Scans the network looking for a server.
    If no server is found, displays an error message and terminates.
    If a server is found, stores its IP address in the global variable base.
    """

    global base
    logger.info("Connecting to server...")
    if (base := networking.find_server(networking.scan())) is None:
        logger.error("Server is not found. Try again later")
        input()
        sys.exit(1)
    else:
        base = f"http://{base}"


@utils.count
def join():
    global token
    """
    Joins the server.

    Parameters:
    No

    Functionality:
    Makes a POST request to /join to the server with id, username, and timestamp.
    Gets the server access token from the response.
    If a TimeoutError occurred, displays an error message and terminates.
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


def users():
    """
    Outputs a list of connected users.

    Options:
    No

    Functionality:
    Makes a GET request to /users on the server.
    Gets a list of connected users in the response.
    Outputs the username and id for each connected user.
    """

    request = r.get(f"{base}/users")
    print("Loggined users:")
    for user in request.json()["users"]:
        print(f"{user['username']} (id: {user['id']})")


def send_message():
    """
    Send user input messages to the server.

    Continuously reads input from the user and sends it as a message
    to the /message endpoint while there are active threads.

    The message data sent contains the user id, timestamp, auth token,
    and message content.

    Any EOFError exceptions are suppressed to avoid crashing on Ctrl+D
    or Ctrl+Z on Windows.
    """
    while threads_active:
        with suppress(EOFError):
            if line := input():
                r.post(
                    f"{base}/message",
                    json={
                        "id": userid,
                        "timestamp": utils.timestamp(),
                        "token": token,
                        "message": line,
                    },
                )


def get_events():
    """
    Fetch and print new events from the server every 5 seconds.

    Continuously polls the /events endpoint to retrieve new events
    while there are active threads.

    The auth token is sent with each request. The 'events' field
    of the JSON response is iterated through to print each event
    using the print_event utility function.

    The threads_active global flag is used to determine when to stop.
    """
    global threads_active
    while threads_active:
        for event in (
            r.get(f"{base}/events", json={"token": token}).json().get("events")
        ):
            utils.print_event(event)
        sleep(5)


colorama.init(autoreset=True)

base = None
token = None
userid = networking.get_my_ip().split(".")[-1]
threads_active = True


if (username := cache.read_from_cache("username")) == "":
    username = input(f"{colorama.Fore.YELLOW}Enter your username: ")
    cache.write_to_cache("username", username)
    utils.clear_console()

logger.info(f"Done in {connect()} seconds...")
logger.info(f"Joined in {join()} seconds...")
users()


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
