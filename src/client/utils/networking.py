import scapy.all as scapy
import socket
import requests as r
from cache import cache


def scan():
    """
    Сканирует сеть и возвращает список IP-адресов устройств.

    Параметры:
    Нет

    Функциональность:
    Создает ARP-запрос для сети, к которой принадлежит IP-адрес клиента.
    Отправляет широковещательный ARP-запрос и получает ответы.
    Извлекает IP-адреса устройств из полученных ответов.
    Возвращает список IP-адресов.
    """
    arp_request = scapy.ARP(pdst=f"{get_my_ip()}/24")
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return [element[1].psrc for element in answered_list]


def get_my_ip():
    """
    Получает IP-адрес клиента.

    Параметры:
    Нет

    Функциональность:
    Создает UDP-сокет.
    Подключается к 8.8.8.8:80 для получения собственного IP-адреса.
    Извлекает IP-адрес из информации о сокете.
    Закрывает сокет.
    Возвращает IP-адрес клиента.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect(("8.8.8.8", 80))

    try:
        return s.getsockname()[0]
    finally:
        s.close()


def find_server(ips: list[str]):
    """
    Ищет сервер среди списка IP-адресов.

    Параметры:
    ips (list[str]): Список IP-адресов для проверки.

    Функциональность:
    Проверяет, есть ли в кэше сохраненный IP-адрес сервера. Если есть и сервер доступен, возвращает его IP-адрес.

    Если в кэше нет IP-адреса сервера или он недоступен, перебирает IP-адреса из списка.
    Если сервер с доступен по какому-либо IP-адресу, сохраняет его в кэше и возвращает.

    Если сервер не найден по ни одному IP-адресу, возвращает None.
    """

    if (ip := cache.read_from_cache("server")) is not None:
        if check_connection(ip):
            return ip

    for ip in ips:
        if check_connection(ip):
            cache.write_to_cache("server", ip)
            return ip

    return None


def check_connection(ip: str) -> bool:
    """
    Проверяет доступность сервера по IP-адресу.

    Параметры:
    ip (str): IP-адрес сервера для проверки.

    Функциональность:
    Пытается сделать GET-запрос к /isvalid на сервере по указанному IP-адресу.
    Если запрос прошел успешно и ответ содержит {"valid": True}, возвращает True.
    Если произошла ошибка TimeoutError, возвращает False.
    Если ответ невозможно декодировать из JSON, возвращает False.
    """

    try:
        print(rf"http://{ip}/isvalid")
        return r.get(rf"http://{ip}/isvalid").json().get("valid", False)
    except (TimeoutError, r.exceptions.JSONDecodeError, r.exceptions.ConnectionError):
        return False
