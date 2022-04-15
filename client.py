from dataclasses import dataclass
from message import *


@dataclass
class Client:
    # TODO need server connection and GUI
    def authentication(self, username: str, password: str):
        pass

    def registration(self, username: str, password: str):
        pass

    def add_contact(self, username: str):
        pass

    def get_contacts(self):
        pass

    def send_message(self, text: str, receiver: str):
        pass

    def get_conversation(self, username: str):
        pass
