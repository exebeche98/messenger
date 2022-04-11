from dataclasses import dataclass
from client import *
from _datetime import datetime
from message import *
from user import *
import uuid


@dataclass
class Server:
    conversations: {}
    users: {}

    def show_all_users(self):
        for user in self.users:
            print(f"{user}")

    def create_user(self, username: str, password: str):
        if username in self.users:
            print(f"User with username {username} already exist, try another username")
        else:
            print(f"User {username} added successful")
            _id = str(uuid.uuid4())
            _user = User(name=username, id=_id, password=password)
            self.users[username] = _user

    def delete_user(self, username: str):
        if username not in self.users:
            print(f"User with nickname: {username} doesn't exist, try another nickname")
        else:
            print(f"User with name {username} deleted")
            del self.users[username]

    def send_message(self, sender: str, receiver: str, message: str):
        #_time = datetime.now().strftime("%d/%m/%y %H:%M")
        _time = datetime.now()
        _msg = Message(time_send=str(_time), text=message, sender=sender, receiver=receiver)

        sender_id = self.users[sender].id
        receiver_id = self.users[receiver].id

        if sender_id + '_' + receiver_id in self.conversations:
            self.conversations[sender_id + '_' + receiver_id].append(_msg)
        elif receiver_id + '_' + sender_id in self.conversations:
            self.conversations[receiver_id + '_' + sender_id].append(_msg)
        else:
            self.conversations[sender_id + '_' + receiver_id] = []
            self.conversations[sender_id + '_' + receiver_id].append(_msg)

    def get_conversation(self, sender: str, receiver: str):
        sender_id = self.users[sender].id
        receiver_id = self.users[receiver].id

        if sender_id + '_' + receiver_id in self.conversations:
            return self.conversations[sender_id + '_' + receiver_id]
        elif receiver_id + '_' + sender_id in self.conversations:
            return self.conversations[receiver_id + '_' + sender_id]
        else:
            print("No such conversation!")



