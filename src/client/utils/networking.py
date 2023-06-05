import scapy.all as scapy
import socket
import requests as r
from cache import cache


def scan():
    arp_request = scapy.ARP(pdst=f"{get_my_ip()}/24")
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return [element[1].psrc for element in answered_list]


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect(("8.8.8.8", 80))

    try:
        return s.getsockname()[0]
    finally:
        s.close()


def find_server(ips: list[str]):
    if (ip := cache.from_cache("server")) is not None:
        if check_connection(ip):
            return ip

    for ip in ips:
        if check_connection(ip):
            cache.to_cache("server", ip)
            return ip

    return None


def check_connection(ip: str) -> bool:
    try:
        print(rf"http://{ip}/isvalid")
        return r.get(rf"http://{ip}/isvalid").json().get("valid", False)
    except TimeoutError:
        return False
    except r.exceptions.JSONDecodeError:
        return False
