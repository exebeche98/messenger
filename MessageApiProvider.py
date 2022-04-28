from typing import Dict, List
import requests


class MessageApiProvider(object):
    def __init__(self, service: str, sender_name: str, receiver_name: str):
        self.__api_url = f'{service}/api/conversation/{sender_name}/{receiver_name}'

    def get_conversation(self) -> List[str]:
        return requests.get(self.__api_url).json()

    def add_message(self, data: Dict[str, str]):
        print(f"MessageApi_add message {data}")
        print(f'{self.__api_url}')
        requests.post(f'{self.__api_url}', json=data)
