from functools import wraps
from sanic.response import json
from sqlalchemy.sql import select

from models import tb_user
from models import tb_session
from models import tb_permission
from models import tb_user_group
from models import tb_group
from models import tb_group_permission
from engine import Connection


async def check_request_for_authorization_status(request):
    session = request.cookies.get('session')
    if session:
        flag = False
        async with Connection() as conn:
            result = await conn.execute(tb_session.select().where(tb_session.c.session_id == session).limit(1))
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
                async with Connection() as conn:
                    j = tb_user\
                        .join(tb_user_group, tb_user.c.user_id == tb_user_group.c.user_id)\
                        .join(tb_group, tb_user_group.c.group_id == tb_group.c.group_id)\
                        .join(tb_group_permission, tb_group.c.group_id == tb_group_permission.c.group_id)\
                        .join(tb_permission, tb_group_permission.c.permission_id == tb_permission.c.permission_id)
                    permissions = await conn.execute(select([tb_permission.c.name]).select_from(j).where(
                        tb_user.c.user_id == request["user_id"]))
                    async for p in permissions:
                        permission = p.name
                        if ability == permission:
                            return await f(request, *args, **kwargs)
                    else:
                        return json({'Status': "You do not have access"}, 403)
            else:
                return json({'Status': 'Not_authorized'}, 403)
        return decorated_function
    return decorator


def authorized_and_user_in_group(group):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = await check_request_for_authorization_status(request)
            if is_authorized:
                async with Connection() as conn:
                    j = tb_user\
                        .join(tb_user_group, tb_user.c.user_id == tb_user_group.c.user_id)\
                        .join(tb_group, tb_user_group.c.group_id == tb_group.c.group_id)
                    groups = await conn.execute(select([tb_group.c.name]).select_from(j).where(
                        tb_user.c.user_id == request["user_id"]))
                    async for g in groups:
                        group_name = g.name
                        if group == group_name:
                            return await f(request, *args, **kwargs)
                    else:
                        return json({'Status': "You do not have access"}, 403)
            else:
                return json({'Status': 'Not_authorized'}, 403)
        return decorated_function
    return decorator
