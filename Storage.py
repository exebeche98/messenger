from message import *
from user import *

import sqlite3
import uuid
from typing import Iterable, Optional

from abc import abstractmethod
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Tuple
import datetime

# TODO logic for conversations and messages
class AbstractStorage(object):
    """
    Определяет интерфейс хранилища пользователей и из сообщений.
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
    def get_user_id(self, username: str):
        raise NotImplemented


    @abstractmethod
    def delete_user(self, username: str):
        raise NotImplemented

    ###########################################################################

    @abstractmethod
    def send_message(self, sender_name: str, receiver_name: str, text: str):
        raise NotImplemented

    @abstractmethod
    def get_all_messages(self) -> Iterable[Message]:
        raise NotImplemented

    @abstractmethod
    def get_two_users_conversation(self, sender: str, receiver: str) -> Iterable[Message]:
        raise NotImplemented


class DatabaseStorage(AbstractStorage):
    """
    Реализация хранилища в базе данных sqlite.
    """

    def __init__(self, path: Path):
        self.__connection = sqlite3.Connection(path,
                                               detect_types=sqlite3.PARSE_DECLTYPES |
                                               sqlite3.PARSE_COLNAMES)
        self.__cursor = self.__connection.cursor()
        self.__cursor.executescript(
            '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                 username text UNIQUE,
                                                 password text,
                                                 phone text);
                                                                                                                                                                            
               CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY,
                                                    message_text text,
                                                    date_send TIMESTAMP,
                                                    from_id INTEGER,
                                                    to_id INTEGER,
                                                    FOREIGN KEY (from_id)  REFERENCES users (id),
                                                    FOREIGN KEY (to_id)  REFERENCES users (id)
                                                    );
            '''
        )

#######################################################################
    def get_users(self) -> Iterable[User]:
        yield from (self.__make_user(row) for row in self.__cursor.execute('SELECT * FROM users'))

    def get_user_by_name(self, _username: str) -> Optional[User]:
        try:
            #  'SELECT * FROM notes WHERE id=:id', {'id': note_id}
            user = self.__cursor.execute('SELECT * FROM users WHERE username=:username', {'username': _username})
            user = self.__make_user(next(user)) # TODO Почему тут должен быть NEXT?
            return user
        except:
            print(f'Can not find user {_username}...')

    def add_user(self, username: str, password: str, phone: str): # TODO добавить условие на пароль
        try:
            _id = uuid.uuid4().int & (1 << 63)-1  # create random int id
            _user = User(id=_id, username=username, password=password, phone=phone)
            self.__cursor.execute(
                'INSERT INTO users VALUES (:id, :username, :password, :phone ) '
                '  ON CONFLICT (id) DO UPDATE SET id=:id, username=:username, password=:password, phone=:phone',
                asdict(_user)
            )
            self.__connection.commit()
        except:
            print(f'Пользоваьель с именем {username} уже существует')

    def delete_user(self, _username: str):
        try:
            self.__cursor.execute('DELETE FROM users WHERE username=:username', {'username': _username})
            self.__connection.commit()
            print(f"User with name {_username} deleted successfully")
        except:
            print(f"Can not delete user with name {_username}...")

    def get_user_id(self, _username: str) -> int | None:
        try:
            _sender_id = self.__cursor.execute('SELECT id FROM users WHERE username=:username', {'username': _username})
            _sender_id = next(_sender_id)
            _sender_id = _sender_id[0]
            return _sender_id
        except:
            print(f"Can not find user{_username}")

#######################################################################

    def send_message(self, sender_name: str, receiver_name: str, text: str):
        try:
            _sender_id = self.__cursor.execute('SELECT id FROM'
                                            ' users WHERE username=:username', {'username': sender_name})
            _sender_id = next(_sender_id)
            _sender_id = _sender_id[0]

            _receiver_id = self.__cursor.execute('SELECT id FROM'
                                              ' users WHERE username=:username', {'username': receiver_name})
            _receiver_id = next(_receiver_id)
            _receiver_id = _receiver_id[0]

            _id = uuid.uuid4().int & (1 << 63) - 1  # create random int id
            now = datetime.datetime.now()
            print(now)
            insertQuery = """INSERT INTO messages VALUES (?, ?, ?, ?, ?);"""
            self.__cursor.execute(insertQuery, (_id, text, now, _sender_id, _receiver_id))
            self.__connection.commit()
            print("Message send!!!")
        except:
            print(f"Can not send message {text[:10]} from {sender_name} to {receiver_name}")

    def get_all_messages(self) -> Iterable[Message]:
        yield from (self.__make_message(row) for row in self.__cursor.execute('SELECT * FROM messages'))

    def get_two_users_conversation(self, sender_name: str, receiver_name: str) -> Iterable[Message]:
        _sender_id = self.__cursor.execute('SELECT id FROM'
                                          ' users WHERE username=:username', {'username': sender_name})
        _sender_id = next(_sender_id)
        _sender_id = _sender_id[0]

        _receiver_id = self.__cursor.execute('SELECT id FROM'
                                            ' users WHERE username=:username', {'username': receiver_name})
        _receiver_id = next(_receiver_id)
        _receiver_id = _receiver_id[0]

        yield from (self.__make_message(row) for row in self.__cursor.execute('SELECT * FROM'
                                                                              ' messages WHERE'
                                                                              '(from_id=:sender_id AND to_id=:receiver_id) OR'
                                                                              '(from_id=:receiver_id AND to_id=:sender_id)',
                                                                              {'sender_id': _sender_id, 'receiver_id':_receiver_id}))


    @staticmethod
    def __make_user(row: Tuple[int, str, str, str]) -> User:
        return User(row[0], row[1], row[2], row[3])

    @staticmethod
    def __make_message(row: Tuple[int, str, datetime.datetime, int, int]) -> Message:
        return Message(row[0], row[1], row[2], row[3], row[4])

