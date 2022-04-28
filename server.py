from Storage import *
from pathlib import Path
from typing import Any, AsyncIterable, Dict, Iterable

from aiohttp import web

import aiohttp_jinja2
import jinja2


routes = web.RouteTableDef()


def __to_list(iterable: AsyncIterable[Any]) -> Iterable[Any]:
    return [item for item in iterable]


@routes.get('/')  # redirect to users list
async def root(_request: web.Request) -> web.Response:
    raise web.HTTPFound(location='/login')


@routes.get('/users/{sender_name}')  # show all users
@aiohttp_jinja2.template('users.jinja2')
async def get_users(request: web.Request) -> Dict[str, Any]:
    storage: AbstractStorage = request.app['storage']
    return {
        'name': 'Users Manager',
        'users': __to_list(storage.get_users()),
        'sender_name': request.match_info['sender_name']
    }


@routes.post('/users/{sender_name}')
@aiohttp_jinja2.template('users.jinja2')
async def select_user(request: web.Request) -> web.Response:
    storage: AbstractStorage = request.app['storage']
    data = dict(await request.post()) # receiver_name
    sender_name = request.match_info['sender_name']
    return web.HTTPFound(location=f'/conversation/{sender_name}/{data["username"]}')


@routes.get('/conversation/{sender_name}/{receiver_name}', allow_head=False) #  Работает
@aiohttp_jinja2.template('conversation.jinja2')
async def conversation(request: web.Request) -> Dict[str, Any]:
    storage: AbstractStorage = request.app['storage']
    sender_name = request.match_info['sender_name']
    receiver_name = request.match_info['receiver_name']
    sender_id = storage.get_user_by_name(sender_name).user_id
    receiver_id = storage.get_user_by_name(receiver_name).user_id

    messages = __to_list(storage.get_two_users_conversation(sender_name, receiver_name))
    messages.sort(key=lambda x: x.date_send)

    return {
        'name': 'Conversation',
        'messages': messages,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'sender_name': sender_name,
        'receiver_name': receiver_name,
        'current_message': ''
    }


@routes.post('/conversation/{sender_name}/{receiver_name}')  # работает
@aiohttp_jinja2.template('conversation.jinja2')
async def send_message(request: web.Request) -> Dict[str, Any]:
    storage: AbstractStorage = request.app['storage']
    data = dict(await request.post())  # message text
    sender_name = request.match_info['sender_name']
    receiver_name = request.match_info['receiver_name']
    storage.send_message(sender_name=sender_name, receiver_name=receiver_name, text=data['message'])
    return web.HTTPFound(location=f'/conversation/{sender_name}/{receiver_name}')


@routes.get('/login')
@aiohttp_jinja2.template('login.jinja2')
async def get_login(request: web.Request) -> web.Response: # работает
    storage: AbstractStorage = request.app['storage']
    return {
        'name': 'Введите данные для входа'
    }


@routes.post('/login')
@aiohttp_jinja2.template('login.jinja2')
async def login_user(request: web.Request) -> web.Response:
    storage: AbstractStorage = request.app['storage']
    data = dict(await request.post())
    try:
        user = storage.get_user_by_name(data['username'])
    except:
        print("No such user")
        raise web.HTTPForbidden()

    if user.password == data['password']:
        print("Login correct")
        return web.HTTPFound(location=f'/users/{data["username"]}')

    else:
        print("Login error")
        raise web.HTTPForbidden()


if __name__ == '__main__':
    settings = {
        'port': 8081,
        'data_storage': {
            'storage': 'storage.db',
        }
    }

    app = web.Application()
    app['storage'] = DatabaseStorage(Path('storage.db'))
    templates_directory = Path(__file__).parent.joinpath('templates')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(templates_directory)))
    app.add_routes(routes)

    # setup_swagger(app, title='Notes API')

    web.run_app(app, port=settings['port'])




