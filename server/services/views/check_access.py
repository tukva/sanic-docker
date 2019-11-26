from sanic.response import json

from services.decorators import authorized_and_user_has, authorized_and_user_in_group


@authorized_and_user_has()
async def is_permission_granted(request):
    return json("Ok", 200)


@authorized_and_user_in_group()
async def is_group_granted(request):
    return json("Ok", 200)
