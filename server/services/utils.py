import uuid

import psycopg2
from sqlalchemy.sql import select
from passlib.hash import bcrypt
from sanic.response import text

from models import _SSO as SSO


async def check_request_for_authorization_status(request, conn):
    session = request.cookies.get('session')
    flag = False
    if session:
        result = await conn.execute(SSO.session.select().where(SSO.session.c.session_id == session))
        row = await result.fetchone()
        if row:
            request["user_id"] = row.user_id
            flag = True
    return flag


async def check_permission(request, conn, permission):
    flag = False
    # Return a Join from this FromClause to another FromClause.
    j = SSO.user \
        .join(SSO.user_group, SSO.user.c.user_id == SSO.user_group.c.user_id) \
        .join(SSO.group, SSO.user_group.c.group_id == SSO.group.c.group_id) \
        .join(SSO.group_permission, SSO.group.c.group_id == SSO.group_permission.c.group_id) \
        .join(SSO.permission, SSO.group_permission.c.permission_id == SSO.permission.c.permission_id)
    # Return a new select() construct with the given FROM expression merged into its list of FROM object.
    permissions = await conn.execute(select([SSO.permission.c.name]).select_from(j).where(
        SSO.user.c.user_id == request["user_id"]))
    async for p in permissions:
        if permission == p.name:
            flag = True
    return flag


async def check_group(request, conn,  group):
    flag = False
    # Return a Join from this FromClause to another FromClause.
    j = SSO.user \
        .join(SSO.user_group, SSO.user.c.user_id == SSO.user_group.c.user_id) \
        .join(SSO.group, SSO.user_group.c.group_id == SSO.group.c.group_id)
    # Return a new select() construct with the given FROM expression merged into its list of FROM objects.
    groups = await conn.execute(select([SSO.group.c.name]).select_from(j).where(
        SSO.user.c.user_id == request["user_id"]))
    async for g in groups:
        if group == g.name:
            flag = True
    return flag


async def do_sign_up(conn, data):
    try:
        user = await conn.execute(SSO.user.insert().values(username=data["username"],
                                                           password=bcrypt.hash(data["password"])))
        row = await user.fetchone()
        await conn.execute(SSO.user_group.insert().values(user_id=row.user_id, group_id=2))
        return text("Ok", 200)
    except psycopg2.Error:
        return text("Username already exists", 423)


async def do_sign_in(conn, data):
    user = await conn.execute(SSO.user.select().where(SSO.user.c.username == data["username"]))
    row = await user.fetchone()
    if not row:
        return text("Wrong username", 423)
    if not bcrypt.verify(data["password"], row.password):
        return text("Wrong password", 423)
    await conn.execute(SSO.session.delete().where(SSO.session.c.user_id == row.user_id))
    session_id = str(uuid.uuid4())
    await conn.execute(SSO.session.insert().values(session_id=session_id, user_id=row.user_id))
    response = text("Ok", 200)
    response.cookies['session'] = session_id
    return response


async def do_sign_out(request, conn):
    await conn.execute(SSO.session.delete().where(SSO.session.c.user_id == request.get("user_id")))
    return text("Ok", 200)


async def do_reset_password(conn, data):
    user = await conn.execute(SSO.user.select().where(SSO.user.c.username == data["username"]))
    row = await user.fetchone()
    if not row:
        return text("Wrong username", 423)
    if not bcrypt.verify(data["old_password"], row.password):
        return text("Wrong old password", 423)
    await conn.execute(SSO.user.update().where(
        SSO.user.c.username == data["username"]).values(
        password=bcrypt.hash(data["new_password"])))
    return text("Ok", 200)
