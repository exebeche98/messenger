from typing import Dict, List
import requests


class UserApiProvider(object):
    def __init__(self, service: str):
        self.__api_url = f'{service}/api/users'

    def get_users(self) -> List[str]:
        return requests.get(self.__api_url).json()
