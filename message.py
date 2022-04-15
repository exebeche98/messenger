from dataclasses import dataclass


@dataclass
class Message:
    id: str
    text: str
    sender: str
    receiver: str
    time_send: str

