from dataclasses import dataclass, field


class Peer:
    """
    A Peer represents a peer on the local network.

    Attributes:
    ip (str): The IP address of the peer.
    username (str): The username of the peer.
    read_messages (list): A list of messages that have been read.
    messages (list): A list of all message data received from peer.

    Methods:
    get_unread(): Returns a list of unread messages
    (messages not in read_messages list).
    """

    ip: str
    username: str
    read_messages: list = field(default_factory=list)
    messages: list = field(default_factory=list)

    def get_unread(self):
        """
        Get a list of unread messages.

        Returns a list of messages that are in the messages list
        but not in the read_messages list.
        """
        return [message for message in self.messages if message not in self.read_messages]
