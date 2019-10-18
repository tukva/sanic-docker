from functools import wraps
from aiopg.sa import create_engine
from sanic.response import json

from db import connection
from models.user import tb_user
from models.session import tb_session


async def check_request_for_authorization_status(request):
    session = request.cookies.get('session')
    if session:
        flag = False
        async with create_engine(connection) as engine:
            async with engine.acquire() as conn:
                result = conn.execute(tb_session.select().where(tb_session.c.session_id == session).limit(1))
                async for r in result:
                    user_id = r.user_id
                    if user_id:
                        request["user_id"] = user_id
                        flag = True
    return flag


# def authorized():
#     def decorator(f):
#         @wraps(f)
#         async def decorated_function(request, *args, **kwargs):
#             is_authorized = await check_request_for_authorization_status(request)
#
#             if is_authorized:
#                 response = await f(request, *args, **kwargs)
#                 return response
#             else:
#                 return json({'Status': 'Not_authorized'}, 403)
#         return decorated_function
#     return decorator


def authorized_and_user_has(ability):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = await check_request_for_authorization_status(request)
            if is_authorized:
                async with create_engine(connection) as engine:
                    async with engine.acquire() as conn:
                        result = conn.execute(
                            tb_user.select().where(tb_user.c.user_id == request.get("user_id")).limit(1))
                        async for r in result:
                            permission = r.permission
                            if ability in permission:
                                return await f(request, *args, **kwargs)
                            else:
                                return json({'Status': "You do not have access"}, 403)
            else:
                return json({'Status': 'Not_authorized'}, 403)
        return decorated_function
    return decorator
