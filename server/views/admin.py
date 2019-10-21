import psycopg2
from aiopg.sa import create_engine
from sanic.response import json
from sanic.exceptions import abort
from marshmallow.exceptions import ValidationError

from db import connection
from models.user_group import tb_user_group
from decorators import authorized_and_user_in_group
from schemas import PermitEditRequestSchema


@authorized_and_user_in_group("admins")
async def permit_edit(request):
    try:
        data = PermitEditRequestSchema().load(request.form)
        async with create_engine(connection) as engine:
            async with engine.acquire() as conn:
                try:
                    await conn.execute(tb_user_group.insert().values(user_id=data["user_id"], group_id=3))
                    return json("Ok", 200)
                except psycopg2.Error as e:
                    abort(400, message=e)
    except (ValidationError, psycopg2.DataError) as e:
        abort(400, message=e)
