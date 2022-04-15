from dataclasses import dataclass


@dataclass
class User:
    id: str  # primary key
    username: str  # super key and сandidate key, username are unique
    password: str

