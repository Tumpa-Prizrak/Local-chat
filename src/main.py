from src.tools import client, server
import threading

ips = client.scan()
print(ips)
print(client.get_list_peers(ips))
