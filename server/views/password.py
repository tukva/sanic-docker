from sanic.response import json
from aiopg.sa import create_engine
from passlib.hash import bcrypt

from db import connection
from decorators import authorized
from models.user import tb_user


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
            result = conn.execute(tb_user.select().where(tb_user.c.username == username).limit(1))
            async for r in result:
                if bcrypt.verify(old_password, r.password):
                    user_id = r.user_id
                    if user_id:
                        result = await conn.execute(tb_user.update().where(tb_user.c.username == username).values(
                            password=bcrypt.hash(new_password)))
                        if result.rowcount:
                            return json("Ok", 200)
            return json("Bad Request", 400)
