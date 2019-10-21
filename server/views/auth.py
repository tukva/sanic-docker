from sanic.response import json
from passlib.hash import bcrypt
import psycopg2.errors

from decorators import authorized_and_user_has
from utils import generate_session_id
from models.user import tb_user
from models.session import tb_session
from models.user_group import tb_user_group
from engine import Connection


async def sign_up(request):
    username = request.form.get('username')
    password = request.form.get('password')
    password_repeat = request.form.get('password_repeat')
    if password != password_repeat:
        return json("Bad Request. Passwords don't match", 400)
    async with Connection() as conn:
        try:
            result = await conn.execute(tb_user.insert().values(username=username,
                                                                password=bcrypt.hash(password)))
            async for r in result:
                user_id = r.user_id
                if user_id:
                    if user_id == 1:
                        await conn.execute(tb_user_group.insert().values(user_id=user_id, group_id=1))
                    else:
                        await conn.execute(tb_user_group.insert().values(user_id=user_id, group_id=2))
                return json("Ok", 200)
        except psycopg2.Error as e:
            return json(e.pgerror, 400)


async def sign_in(request):
    username = request.form.get('username')
    password = request.form.get('password')
    async with Connection() as conn:
        result = await conn.execute(tb_user.select().where(tb_user.c.username == username).limit(1))
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


@authorized_and_user_has("view")
async def sign_out(request):
    async with Connection() as conn:
        await conn.execute(tb_session.delete().where(tb_session.c.user_id == request.get("user_id")))
        return json("Ok", 200)
