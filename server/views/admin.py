import psycopg2
from sanic.response import json
from sanic.exceptions import abort
from marshmallow.exceptions import ValidationError

from models.user_group import tb_user_group
from decorators import authorized_and_user_in_group
from engine import Connection
from schemas import PermitEditSchema


@authorized_and_user_in_group("admins")
async def permit_edit(request):
    try:
        data = PermitEditSchema().load(request.form)
        async with Connection() as conn:
            try:
                await conn.execute(tb_user_group.insert().values(user_id=data["user_id"], group_id=3))
                return json("Ok", 200)
            except psycopg2.Error as e:
                abort(400, message=e)
    except (ValidationError, psycopg2.DataError) as e:
        abort(400, message=e)
