from sanic.response import json

from engine import Connection
from services.utils import check_request_for_authorization_status, check_permission, check_group


async def check_auth(request):
    async with Connection() as conn:
        if not await check_request_for_authorization_status(request, conn):
            return json({'Status': 'Not_authorized'}, 401)
        return json("Ok", 200)


async def check_auth_and_user_has(request):
    async with Connection() as conn:
        if not await check_request_for_authorization_status(request, conn):
            return json({'Status': 'Not_authorized'}, 401)
        permission = request.json.get("permission")
        if not await check_permission(request, conn, permission):
            return json({'Status': "You do not have access"}, 403)
        return json("Ok", 200)


async def check_auth_and_user_in_group(request):
    async with Connection() as conn:
        if not await check_request_for_authorization_status(request, conn):
            return json({'Status': 'Not_authorized'}, 401)
        group = request.json.get("group")
        if not await check_group(request, conn, group):
            return json({'Status': "You do not have access"}, 403)
        return json("Ok", 200)
