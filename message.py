import datetime
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Message:
    message_id: int # TODO make message_id
    message_text: str
    date_send: datetime.datetime
    from_id: int
    to_id: int

    def to_json(self) -> Dict[str, Any]:
        return {
            'message_id': str(self.message_id),
            'message_text': self.message_text,
            'date_send': self.date_send.strftime('%b %d %Y %H:%M'),
            'from_id': self.from_id,
            'to_id': self.to_id
        }