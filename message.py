import datetime
from dataclasses import dataclass


@dataclass
class Message:
    id: int # TODO make message_id
    message_text: str
    date_send: datetime.datetime
    from_id: int
    to_id: int
    # TODO make to json function
