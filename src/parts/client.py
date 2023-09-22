from src.tools import networking, datatypes


def main():
    """
    Main function for client program.

    Functionality:

    1. Get list of available peers on the network.
    2. Prompt user to enter their nickname.
    3. Loop through each peer and send a "hello" message
       with the user's nickname.
    4. Enter infinite loop to keep client running.

    Parameters:

    peers (list[Peer]): List of discovered peers.
    name (str): The user's nickname.

    """
    peers: list[datatypes.Peer] = networking.get_available_peers()
    name: str = input("Enter your nickname: ")
    for peer in peers:
        networking.send_data(peer.ip, name, "hello", name)

    while True:
        pass
