import psycopg2
from sanic.exceptions import abort
from sanic.response import json
from aiopg.sa import create_engine
from passlib.hash import bcrypt
from marshmallow.exceptions import ValidationError

from db import connection
from decorators import authorized_and_user_has
from models.user import tb_user
from schemas import ResetPasswordSchema


@authorized_and_user_has("edit")
async def reset_password(request):
    try:
        data = ResetPasswordSchema().load(request.form)
        if data["new_password"] != data["new_password_repeat"]:
            return json("Bad Request. New passwords don't match", 400)
        async with create_engine(connection) as engine:
            async with engine.acquire() as conn:
                result = conn.execute(tb_user.select().where(tb_user.c.username == data["username"]).limit(1))
                async for r in result:
                    if bcrypt.verify(data["old_password"], r.password):
                        user_id = r.user_id
                        if user_id:
                            result = await conn.execute(tb_user.update().where(
                                tb_user.c.username == data["username"]).values(
                                password=bcrypt.hash(data["new_password"])))
                            if result.rowcount:
                                return json("Ok", 200)
                return json("Bad Request", 400)
    except (ValidationError, psycopg2.DataError) as e:
        abort(400, message=e)
