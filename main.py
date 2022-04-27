# from server import *
# from client import *
# #
from Storage import *
from pathlib import Path

if __name__ == '__main__':

    storage = DatabaseStorage(Path('storage.db'))
    storage.add_user(username='Alice', password='123', phone='123')
    storage.add_user(username='Bob', password='123', phone='123')
    storage.add_user(username='Ivan', password='123', phone='123')
    storage.add_user(username='Алиса', password='123', phone='123')
    storage.add_user(username='Боб', password='123', phone='123')
    storage.add_user(username='Steve', password='123', phone='123')

    print('All users:')

    for user in storage.get_users():
        print(user)

    storage.send_message(sender_name="Bob", receiver_name="Alice", text="Hello")
    storage.send_message(sender_name="Alice", receiver_name="Bob", text="Hello")

    storage.send_message(sender_name="Ivan", receiver_name="Bob", text="Hello Bob, that's Ivan")
    storage.send_message(sender_name="Bob", receiver_name="Ivan", text="Hello Ivan")
    print('All messages:')
    for message in storage.get_two_users_conversation("Alice", "Bob"):
        print(message)

    for message in storage.get_two_users_conversation("Bob", "Ivan"):
        print(message)

