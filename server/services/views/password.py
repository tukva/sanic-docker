import psycopg2
from sanic.exceptions import abort
from sanic.response import json
from passlib.hash import bcrypt
from marshmallow.exceptions import ValidationError

from services.decorators import authorized
from models import tb_user
from engine import Connection
from services.forms import ResetPasswordSchema


@authorized()
async def reset_password(request):
    try:
        data = ResetPasswordSchema().load(request.form)
        if data["new_password"] != data["new_password_repeat"]:
            return json("Locked. New passwords don't match", 423)
        async with Connection() as conn:
            result = await conn.execute(tb_user.select().where(tb_user.c.username == data["username"]).limit(1))
            async for r in result:
                if bcrypt.verify(data["old_password"], r.password):
                    user_id = r.user_id
                    if user_id:
                        result = await conn.execute(tb_user.update().where(
                            tb_user.c.username == data["username"]).values(
                            password=bcrypt.hash(data["new_password"])))
                        if result.rowcount:
                            return json("Ok", 200)
            return json("Locked", 423)
    except (ValidationError, psycopg2.DataError) as e:
        abort(400, message=e)
