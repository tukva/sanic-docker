from sanic.response import json

from models.user_group import tb_user_group
from decorators import authorized_and_user_in_group
from engine import Connection


@authorized_and_user_in_group("admins")
async def permit_edit(request):
    user_id = request.form.get('user_id')
    async with Connection() as conn:
        await conn.execute(tb_user_group.insert().values(user_id=user_id, group_id=3))
        return json("Ok", 200)
