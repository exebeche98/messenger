from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class User:
    user_id: int
    username: str
    password: str
    phone: str

    def to_json(self) -> Dict[str, Any]:
        return {
            'user_id': str(self.user_id),
            'username:': self.username,
            'password': self.password,
            'phone' : self.phone,
        }
