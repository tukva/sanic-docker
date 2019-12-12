from http import HTTPStatus

from sanic.response import json

from services.utils import check_request_for_authorization_status, check_permission, check_group, get_user_permissions


async def check_auth(request):
    if not await check_request_for_authorization_status(request):
        return json({'Status': 'Not_authorized'}, HTTPStatus.UNAUTHORIZED)
    return json("Ok", HTTPStatus.OK)


async def check_auth_and_user_has(request):
    if not await check_request_for_authorization_status(request):
        return json({'Status': 'Not_authorized'}, HTTPStatus.UNAUTHORIZED)
    permission = request.json.get("permission")
    if not await check_permission(request, permission):
        return json({'Status': "You do not have access"}, HTTPStatus.FORBIDDEN)
    return json("Ok", HTTPStatus.OK)


async def check_auth_and_user_in_group(request):
    if not await check_request_for_authorization_status(request):
        return json({'Status': 'Not_authorized'}, HTTPStatus.UNAUTHORIZED)
    group = request.json.get("group")
    if not await check_group(request, group):
        return json({'Status': "You do not have access"}, HTTPStatus.FORBIDDEN)
    return json("Ok", HTTPStatus.OK)


async def check_auth_and_get_user_permissions(request):
    if not await check_request_for_authorization_status(request):
        return json({'Status': 'Not_authorized'}, HTTPStatus.UNAUTHORIZED)

    permissions = await get_user_permissions(request)
    resp = {"permissions": permissions}
    print(resp)
    return json(resp, HTTPStatus.OK)
