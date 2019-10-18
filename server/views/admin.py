from aiopg.sa import create_engine
from sanic.response import json

from db import connection
from models.user import tb_user
from decorators import authorized_and_user_has


@authorized_and_user_has("all")
async def permit_edit(request, user_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            await conn.execute(
                tb_user.update().where(tb_user.c.user_id == user_id).values({tb_user.c.permission[0]: "edit"}))
            return json("Ok", 200)
