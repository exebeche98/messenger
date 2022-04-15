from abc import abstractmethod
from typing import Iterable, Optional
from _datetime import datetime

import uuid
from message import *
from user import *
from conversation import *

# TODO add contacts
class AbstractStorage(object):
    """
    Определяет интерфейс хранилища пользователей их контаков, и переписок.
    Список контактов пользователя хранится на сервере.
    """

    @abstractmethod
    def get_users(self) -> Iterable[User]:
        raise NotImplemented

    @abstractmethod
    def get_user_by_name(self, username: str) -> Optional[User]:
        raise NotImplemented

    @abstractmethod
    def add_user(self, username: str, password: str):
        raise NotImplemented

    @abstractmethod
    def delete_user(self, username: str):
        raise NotImplemented

    ###########################################################################

    @abstractmethod
    def get_conversations(self) -> Iterable[Conversation]:
        raise NotImplemented

    @abstractmethod
    def get_conversation(self, conv_id: str) -> Optional[Conversation]:
        raise NotImplemented

    @abstractmethod
    def add_conversation(self, sender: str, receiver: str) -> None:
        raise NotImplemented

    @abstractmethod
    def delete_conversation(self, user_id: str):
        raise NotImplemented

    @abstractmethod
    def send_message(self, sender: str, receiver: str, text: str):
        raise NotImplemented


class BaseStorage(object):
    """
    Базовый класс хранилища пользователей, контактов и переписок (содержит только данные).
    """

    def __init__(self):
        self._conversations = {}
        self._users = {}
        self._contacts = {}


class ReadWriteStorage(AbstractStorage, BaseStorage):
    def get_users(self) -> Iterable[User]:
        return self._users

    def get_user_by_name(self, username: str) -> Optional[User ]:
        if username in self._users:
            return self._users[username]
        else:
            print(f"No user {username}")

    def add_user(self, username: str, password: str):
        if username in self.users:
            print(f"User with username {username} already exist, try another username")
        else:
            _id = str(uuid.uuid4())
            _user = User(name=username, id=_id, password=password)
            self.users[username] = _user
            print(f"User {username} added successful")

    def delete_user(self, username: str):
        if username not in self._users:
            print(f"User with nickname: {username} doesn't exist, try another nickname")
        else:
            print(f"User with name {username} deleted")
            del self._users[username]

    def get_conversations(self) -> Iterable[Conversation]:
        return self._conversations

    def get_conversation(self, conv_id: str) -> Conversation | None:
        if conv_id in self._conversations:
            return self._conversations[conv_id]
        else:
            return None

    def add_conversation(self, sender: str, receiver: str):
        sender_id = self._users[sender].id
        receiver_id = self._users[receiver].id

        id_1 = sender_id + ' ' + receiver_id
        id_2 = receiver_id + ' ' + sender_id

        if self.get_conversation(id_1) is None and self.get_conversation(id_2) is None:
            self._conversations[id_1] = []
        else:
            print("This conversation already exist")

    def delete_conversation(self, conversation_id: str):
        if conversation_id not in self._conversations:
            print(f"Conversation_id: {conversation_id} doesn't exist, try another conversation_id")
        else:
            print(f"User with name {conversation_id} deleted")
            del self._conversations[conversation_id]

    def send_message(self, sender: str, receiver: str, text: str):
        sender_id = self._users[sender].id
        receiver_id = self._users[receiver].id

        _time = datetime.now()
        _msg = Message(time_send=str(_time), text=text, sender=sender, receiver=receiver)

        id_1 = sender_id + ' ' + receiver_id
        id_2 = receiver_id + ' ' + sender_id

        if self.get_conversation(id_1) is not None:
            self._conversations[id_1].append(_msg)
        elif self.get_conversation(id_2) is not None:
            self._conversations[id_2].append(_msg)
        else:
            self._conversations[id_1] = []
            self._conversations[id_1].append(_msg)



