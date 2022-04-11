from dataclasses import dataclass


@dataclass
class Message:
    text: str
    sender: str
    receiver: str
    time_send: str

