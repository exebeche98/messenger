import datetime
from dataclasses import dataclass


@dataclass
class Message:
    id: int
    message_text: str
    date_send: datetime.datetime
    from_id: int
    to_id: int

