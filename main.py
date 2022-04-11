from server import *
from client import *


if __name__ == '__main__':
    server = Server(users={}, conversations={})
    server.create_user(username='Alice', password='123')
    server.create_user(username='Bob', password='123')
    server.create_user(username='Bob', password='123')
    server.create_user(username='Ivan', password='123')
    #
    server.show_all_users()
    server.delete_user('Ivan')
    server.show_all_users()
    #
    server.send_message('Alice', 'Bob', 'Hello')
    server.send_message('Bob', 'Alice', 'Hello')
    #
    print(server.get_conversation('Alice', 'Bob'))
    print(server.get_conversation('Alice', 'Bob'))


