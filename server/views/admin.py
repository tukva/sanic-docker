from aiopg.sa import create_engine
from sanic.response import json

from db import connection
from models.user_group import tb_user_group
from decorators import authorized_and_user_in_group


@authorized_and_user_in_group("admins")
async def permit_edit(request):
    user_id = request.form.get('user_id')
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            await conn.execute(tb_user_group.insert().values(user_id=user_id, group_id=3))
            return json("Ok", 200)
