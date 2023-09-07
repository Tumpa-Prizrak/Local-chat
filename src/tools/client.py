import scapy.all as scapy
import socket
from src import config


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


def scan():
    """
    Scans the network and returns a list of device IP addresses.

    Parameters:
    No

    Functionality:
    Creates an ARP request for the network to which the client IP address belongs.
    Sends a broadcast ARP request and receives responses.
    Extracts device IP addresses from the received responses.
    Returns a list of IP addresses.
    """
    arp_request = scapy.ARP(pdst=f"{get_my_ip()}/24")
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast / arp_request
    answered_list = [ip for i in scapy.srp(arp_request_broadcast, timeout=1, verbose=False) for ip in i]

    return list({element[1].psrc for element in answered_list})


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


def get_list_peers(ips):
    """
    Get a list of connected peer sockets.

    Parameters:
    ips (list): A list of IP addresses to check for connections.

    Returns:
    list: A list of connected socket objects.

    Functionality:
    Iterates through the provided list of IP addresses.
    Attempts to create a socket connection to each IP.
    Filters out any IPs that did not connect.
    Returns a list of the connected socket objects.
    """
    return [sock for ip in ips if (sock := connection(ip)) is not None]


def connection(ip: str):
    """
    Create a socket connection to the given IP address.

    Parameters:
    ip (str): The IP address to connect to.

    Returns:
    socket: The connected socket object if successful, None otherwise.

    Functionality:
    Creates a TCP socket.
    Tries to connect to the IP on port specified in config.PORT.
    Returns the connected socket on success.
    Catches any exceptions and returns None.
    Closes the socket before returning in all cases.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, config.PORT))
        return ip
    except Exception as e:
        return None
    finally:
        s.close()


def send_data(ip: str, data: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, config.PORT))
