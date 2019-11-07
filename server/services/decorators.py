from functools import wraps
from sanic.response import json

from engine import Connection
from services.utils import check_request_for_authorization_status, check_group, check_permission


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            async with Connection() as conn:
                if not await check_request_for_authorization_status(request, conn):
                    return json({'Status': 'Not_authorized'}, 401)
                response = await f(request, *args, **kwargs)
                return response
        return decorated_function
    return decorator


def authorized_and_user_has(permission):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            async with Connection() as conn:
                if not await check_request_for_authorization_status(request, conn):
                    return json({'Status': 'Not_authorized'}, 401)
                if not await check_permission(request, conn, permission):
                    return json({'Status': "You do not have access"}, 403)
                return await f(request, *args, **kwargs)
        return decorated_function
    return decorator


def authorized_and_user_in_group(group):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            async with Connection() as conn:
                if not await check_request_for_authorization_status(request, conn):
                    return json({'Status': 'Not_authorized'}, 401)
                if not await check_group(request, conn, group):
                    return json({'Status': "You do not have access"}, 403)
                return await f(request, *args, **kwargs)
        return decorated_function
    return decorator
