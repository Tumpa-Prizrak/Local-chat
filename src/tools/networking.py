import socket
import json
import threading
from src import config
from src.tools.datatypes import Peer


class SocketWrapper(socket.socket):
    """
    A wrapper for socket connections to enable use with context managers.

    Parameters:
    *args: Positional arguments to pass to the socket constructor.
    ip (str): The IP address to connect to.
    port (int): The port to connect to.

    Functionality:
    The __init__ method calls the socket constructor and connects to the
    provided IP and port.

    The __enter__ method enables use as a context manager, returning self.

    The __exit__ method closes the socket when exiting the context.
    """

    def __init__(self, *args, ip: str, port: int):
        super().__init__(*args)
        self.connect((ip, port))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_available_peers():
    """
    Scan the local network and find available peers.

    Parameters:
    None

    Returns:
    available_ips (list of datatypes.Peer): List of available peers found

    Functionality:
    1. available_ips starts as an empty list to hold results
    2. _scan_ip attempts to connect to the given IP address:
       - Create a TCP socket
       - Set a timeout of 0.5 seconds
       - Try to connect to the IP and config.PORT
       - Receive data from the socket
       - Close the socket
       - If the data contains a valid username, create a Peer object
         and add it to available_ips
    3. _scan_network scans the local network:
       - Get the first 3 octets of the current IP address
       - Loop from 1 to 255 for the last octet
       - For each IP, start a thread running _scan_ip
       - Join all threads back together
    4. Return the available_ips list containing any discovered peers
    """

    available_ips = []

    def _scan_ip(ip: str):
        nonlocal available_ips
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((ip, config.PORT))
            data = s.recv(1024)
            s.close()
            json_data = json.loads(data)
            if "username" in json_data:
                available_ips.append(Peer(ip, json_data.get("username")))
        except:
            return

    def _scan_network():
        threads = []
        base = ".".join(get_my_ip().split(".")[:3])
        for i in range(1, 255):
            ip = f"{base}.{i}"
            # print(ip)
            t = threading.Thread(target=_scan_ip, args=(ip,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    _scan_network()
    return available_ips


def get_my_ip():
    """
    Gets the IP address of the client.

    Parameters:
    No

    Functionality:
    Creates a UDP socket.
    Connects to 8.8.8.8.8:80 to obtain its own IP address.
    Extracts the IP address from the socket information.
    Closes the socket.
    Returns the IP address of the client.
    """

    with SocketWrapper(socket.AF_INET, socket.SOCK_DGRAM, ip="8.8.8.8", port=80) as s:
        return s.getsockname()[0]


def send_data(ip: str, name: str, command: str, *args):
    """
    Send data to a peer over TCP.

    Parameters:
    ip (str): The IP address of the peer to send data to.
    name (str): The name of the sender.
    command (str): The command to send.
    *args: Any additional arguments to include in the message.

    Returns:
    None

    Functionality:
    Opens a TCP socket connection to the given IP and port.
    Format the message to send over the socket

    The message format is:
    {name} {command.upper()} {args}/e

    Where:

    {name} is the name of the sender
    {command.upper()} converts the command to uppercase
    {args} joins any additional arguments into a space-separated string
    /e is a delimiter to indicate the end of the message

    For example, if name = "Alice", command = "message", and args = ["Hi", "there!"]
    The formatted message would be:
    "Alice MESSAGE Hi there!/e"

    This formats the message in a consistent way so the receiver can
    parse it by splitting on the "/e" delimiter. Converting the command
    to uppercase makes it stand out from the other words.

    Sends the message over the socket.
    Closes the socket when done.
    """
    with SocketWrapper(
        socket.AF_INET, socket.SOCK_STREAM, ip=ip, port=config.PORT
    ) as s:
        s.send(f"{name} {command.upper()} {' '.join(args)}/e")
