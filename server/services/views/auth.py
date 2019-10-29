import psycopg2
from sanic.response import json
from sanic.exceptions import abort
from passlib.hash import bcrypt
from marshmallow.exceptions import ValidationError

from services.decorators import authorized_and_user_has
from services.utils import generate_session_id
from services.forms import SignupSchema, SigninSchema
from models import tb_user
from models import tb_session
from models import tb_user_group
from engine import Connection


async def sign_up(request):
    try:
        data = SignupSchema().load(request.form)
        if data["password"] != data["password_repeat"]:
            return json("Bad Request. Passwords don't match", 400)
        async with Connection() as conn:
            try:
                result = await conn.execute(tb_user.insert().values(username=data["username"],
                                                                    password=bcrypt.hash(data["password"])))
                async for r in result:
                    user_id = r.user_id
                    if user_id:
                        if user_id == 1:
                            await conn.execute(tb_user_group.insert().values(user_id=user_id, group_id=1))
                            await conn.execute(tb_user_group.insert().values(user_id=user_id, group_id=2))
                            await conn.execute(tb_user_group.insert().values(user_id=user_id, group_id=3))
                        else:
                            await conn.execute(tb_user_group.insert().values(user_id=user_id, group_id=2))
                    return json("Ok", 200)
            except psycopg2.Error as e:
                abort(400, message=e)
    except (ValidationError, psycopg2.DataError) as e:
        abort(400, message=e)


async def sign_in(request):
    try:
        data = SigninSchema().load(request.form)
        async with Connection() as conn:
            result = await conn.execute(tb_user.select().where(tb_user.c.username == data["username"]).limit(1))
            async for r in result:
                if bcrypt.verify(data["password"], r.password):
                    user_id = r.user_id
                    if user_id:
                        session_id = generate_session_id()
                        await conn.execute(tb_session.insert().values(session_id=session_id, user_id=user_id))
                        response = json("Ok", 200)
                        response.cookies['session'] = session_id
                        return response
            return json("Bad Request", 400)
    except (ValidationError, psycopg2.DataError) as e:
        abort(400, message=e)


@authorized_and_user_has("view")
async def sign_out(request):
    async with Connection() as conn:
        await conn.execute(tb_session.delete().where(tb_session.c.user_id == request.get("user_id")))
        return json("Ok", 200)