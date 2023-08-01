import scapy.all as scapy
import socket
import requests as r
from cache import cache


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
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return [element[1].psrc for element in answered_list]


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

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect(("8.8.8.8", 80))

    try:
        return s.getsockname()[0]
    finally:
        s.close()


def find_server(ips: list[str]):
    """
    Searches for a server among a list of IP addresses.

    Parameters:
    ips (list[str]): A list of IP addresses to check.

    Functionality:
    Checks if there is a stored IP address of the server in the cache. If there is and the server is available, returns its IP address.

    If there is no IP address of the server in the cache or it is unavailable, it tries IP addresses from the list.
    If a server is available at any IP address, stores it in the cache and returns it.

    If the server is not found at any IP address, returns None.
    """

    if (ip := cache.read_from_cache("server")) != "":
        if check_connection(ip):
            return ip

    for ip in ips:
        if check_connection(ip):
            cache.write_to_cache("server", ip)
            return ip

    return None


def check_connection(ip: str) -> bool:
    """
    Checks the availability of the server by IP address.

    Parameters:
    ip (str): The IP address of the server to check.

    Functionality:
    Attempts to make a GET request to /isvalid on the server at the specified IP address.
    If the request succeeds and the response contains {"valid": True}, returns True.
    If a TimeoutError occurred, returns False.
    If the response cannot be decoded from JSON, returns False.
    """

    try:
        print(rf"http://{ip}/isvalid")
        return r.get(rf"http://{ip}/isvalid").json().get("valid", False)
    except (TimeoutError, r.exceptions.JSONDecodeError, r.exceptions.ConnectionError):
        return False
