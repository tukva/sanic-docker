from aiopg.sa import create_engine
import sqlalchemy as sa
from sqlalchemy.sql import and_

from sanic import Sanic
from sanic.response import json


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
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('username', sa.String(255),
                           nullable=False, unique=True),
                 sa.Column('password', sa.String(255), nullable=False))


app = Sanic(name=__name__)


@app.listener('before_server_start')
async def prepare_db(app, loop):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            await conn.execute('DROP TABLE IF EXISTS users')
            await conn.execute('''CREATE TABLE users (
                                id serial PRIMARY KEY,
                                username varchar(255) NOT NULL UNIQUE, 
                                password varchar(255) NOT NULL)''')


@app.route('/sign_up', methods=["POST"])
async def sign_up(request):
    username = request.form.get('username')
    password = request.form.get('password')
    password_repeat = request.form.get('password_repeat')
    if password != password_repeat:
        return json("passwords don't match")
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            await conn.execute(users.insert().values(username=username,
                                                     password=password))
            return json("ok")


@app.route('/sign_in', methods=["POST"])
async def sign_in(request):
    username = request.form.get('username')
    password = request.form.get('password')
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            result = conn.execute(users.select().where(and_(
                users.c.username == username,
                users.c.password == password)).limit(1))
            async for r in result:
                user_id = r.id
                if user_id:
                    return json("ok")
            return json("incorrect data")


# @app.route('/sign_out', methods=["POST"])
# async def sign_out(request):
#     return json("incorrect data")


@app.route('/reset_password', methods=["POST"])
async def reset_password(request):
    username = request.form.get('username')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    new_password_repeat = request.form.get('new_password_repeat')
    if new_password != new_password_repeat:
        return json("passwords don't match")
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            result = await conn.execute(users.update().where(and_(
                users.c.username == username,
                users.c.password == old_password)
            ).values(password=new_password))
            if result.rowcount:
                return json("ok")
            return json("incorrect data")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
