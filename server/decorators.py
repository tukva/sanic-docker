from functools import wraps
from aiopg.sa import create_engine
from sanic.response import json
from sqlalchemy.sql import select

from db import connection
from models.user import tb_user
from models.session import tb_session
from models.permission import tb_permission
from models.user_group import tb_user_group
from models.group import tb_group
from models.group_permission import tb_group_permission


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
                        j = tb_user\
                            .join(tb_user_group, tb_user.c.user_id == tb_user_group.c.user_id)\
                            .join(tb_group, tb_user_group.c.group_id == tb_group.c.group_id)\
                            .join(tb_group_permission, tb_group.c.group_id == tb_group_permission.c.group_id)\
                            .join(tb_permission, tb_group_permission.c.permission_id == tb_permission.c.permission_id)
                        result = conn.execute(select([tb_permission.c.name]).select_from(j)
                                              .where(tb_user.c.user_id == request["user_id"]))
                        async for r in result:
                            permission = r.name
                            if ability == permission:
                                return await f(request, *args, **kwargs)
                        else:
                            return json({'Status': "You do not have access"}, 403)
            else:
                return json({'Status': 'Not_authorized'}, 403)
        return decorated_function
    return decorator


def authorized_and_user_in_group(ability):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = await check_request_for_authorization_status(request)
            if is_authorized:
                async with create_engine(connection) as engine:
                    async with engine.acquire() as conn:
                        j = tb_user\
                            .join(tb_user_group, tb_user.c.user_id == tb_user_group.c.user_id)\
                            .join(tb_group, tb_user_group.c.group_id == tb_group.c.group_id)
                        result = conn.execute(select([tb_group.c.name]).select_from(j).where(
                            tb_user.c.user_id == request["user_id"]))
                        async for r in result:
                            group = r.name
                            if ability == group:
                                return await f(request, *args, **kwargs)
                        else:
                            return json({'Status': "You do not have access"}, 403)
            else:
                return json({'Status': 'Not_authorized'}, 403)
        return decorated_function
    return decorator
