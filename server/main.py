import random
import string
from functools import wraps

from sanic import Sanic
from sanic.response import json, redirect
from aiopg.sa import create_engine
import sqlalchemy as sa
from passlib.hash import bcrypt
import psycopg2.errors

database_name = 'test'
database_host = 'database'
database_user = 'test'
database_password = 'test'

connection = 'postgres://{0}:{1}@{2}/{3}'.format(database_user,
                                                 database_password,
                                                 database_host,
                                                 database_name)
metadata = sa.MetaData()

users = sa.Table('users', metadata,
                 sa.Column('user_id', sa.Integer, primary_key=True),
                 sa.Column('username', sa.String(255),
                           nullable=False, unique=True),
                 sa.Column('password', sa.String(255), nullable=False),
                 sa.Column("permission", sa.ARRAY(sa.String(50))))

tb_session = sa.Table('tb_session', metadata,
                      sa.Column('session_id', sa.String(255)),
                      sa.Column('user_id', sa.Integer, nullable=False, unique=True))

app = Sanic(name=__name__)


def generate_session_id():
    return ''.join([random.choices(string.digits + string.ascii_letters)[0] for x in range(32)])


async def check_request_for_authorization_status(request):
    session = request.cookies.get('session')
    if session:
        flag = False
        async with create_engine(connection) as engine:
            async with engine.acquire() as conn:
                result = conn.execute(users.select().where(tb_session.c.session_id == session).limit(1))
                async for r in result:
                    user_id = r.user_id
                    if user_id:
                        request["user_id"] = user_id
                        flag = True
    return flag


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = await check_request_for_authorization_status(request)

            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                response = json({'Status': 'Not_authorized'}, 403)
                return response.redirect('/sign_in')
        return decorated_function
    return decorator


@app.listener('before_server_start')
async def prepare_db(app, loop):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            await conn.execute('DROP TABLE IF EXISTS users')
            await conn.execute('''CREATE TABLE users (
                                user_id serial PRIMARY KEY,
                                username varchar(255) NOT NULL UNIQUE, 
                                password varchar(255) NOT NULL,
                                permission TEXT [])''')
            await conn.execute('DROP TABLE IF EXISTS tb_session')
            await conn.execute('''CREATE TABLE tb_session (
                                            session_id varchar(255),
                                            user_id INTEGER NOT NULL)''')


@app.route('/sign_up', methods=["POST"])
async def sign_up(request):
    username = request.form.get('username')
    password = request.form.get('password')
    password_repeat = request.form.get('password_repeat')
    if password != password_repeat:
        return json("Bad Request. Passwords don't match", 400)
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            try:
                result = await conn.execute(users.insert().values(username=username,
                                                                  password=bcrypt.hash(password),
                                                                  permission=["view"]))
                async for r in result:
                    user_id = r.user_id
                    if user_id:
                        if user_id == 1:
                            await conn.execute(
                                users.update().where(users.c.user_id == user_id).values(permission=["admin"]))
                    return json("Ok", 200)
            except psycopg2.Error as e:
                return json(e.pgerror, 400)


@app.route('/sign_in', methods=["POST"])
async def sign_in(request):
    username = request.form.get('username')
    password = request.form.get('password')
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            result = conn.execute(users.select().where(users.c.username == username).limit(1))
            async for r in result:
                if bcrypt.verify(password, r.password):
                    user_id = r.user_id
                    if user_id:
                        session_id = generate_session_id()
                        await conn.execute(tb_session.insert().values(session_id=session_id, user_id=user_id))
                        response = json("Ok", 200)
                        response.cookies['session'] = session_id
                        return response
            return json("Bad Request", 400)


@app.route('/sign_out', methods=["POST"])
@authorized()
async def sign_out(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            await conn.execute(tb_session.delete().where(tb_session.c.user_id == request.get("user_id")))
            return json("Ok", 200)


@app.route('/reset_password', methods=["PATCH"])
@authorized()
async def reset_password(request):
    username = request.form.get('username')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    new_password_repeat = request.form.get('new_password_repeat')
    if new_password != new_password_repeat:
        return json("Bad Request. New passwords don't match", 400)
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            result = conn.execute(users.select().where(users.c.username == username).limit(1))
            async for r in result:
                if bcrypt.verify(old_password, r.password):
                    user_id = r.user_id
                    if user_id:
                        result = await conn.execute(users.update().where(users.c.username == username).values(
                            password=bcrypt.hash(new_password)))
                        if result.rowcount:
                            return json("Ok", 200)
            return json("Bad Request", 400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
