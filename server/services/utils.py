import uuid

from sqlalchemy.sql import select
from passlib.hash import bcrypt

from models import SSOModels
from engine import Connection


async def check_request_for_authorization_status(request):
    async with Connection() as conn:
        session = request.cookies.get('session')
        flag = False
        if session:
            result = await conn.execute(SSOModels.session.select().where(SSOModels.session.c.session_id == session))
            row = await result.fetchone()
            if row:
                request["user_id"] = row.user_id
                flag = True
        return flag


async def check_permission(request, permission):
    async with Connection() as conn:
        flag = False
        join = join_user_permission()
        # Return a new select() construct with the given FROM expression merged into its list of FROM object.
        permissions = await conn.execute(select([SSOModels.permission.c.name]).select_from(join).where(
            SSOModels.user.c.user_id == request["user_id"]))
        async for perm in permissions:
            if permission == perm.name:
                flag = True
        return flag


async def check_group(request, group):
    async with Connection() as conn:
        flag = False
        # Return a Join from this FromClause to another FromClause.
        j = SSOModels.user \
            .join(SSOModels.user_group, SSOModels.user.c.user_id == SSOModels.user_group.c.user_id) \
            .join(SSOModels.group, SSOModels.user_group.c.group_id == SSOModels.group.c.group_id)
        # Return a new select() construct with the given FROM expression merged into its list of FROM objects.
        groups = await conn.execute(select([SSOModels.group.c.name]).select_from(j).where(
            SSOModels.user.c.user_id == request["user_id"]))
        async for g in groups:
            if group == g.name:
                flag = True
        return flag


async def get_user_permissions(request):
    async with Connection() as conn:
        join = join_user_permission()
        # Return a new select() construct with the given FROM expression merged into its list of FROM object.
        select_permissions = await conn.execute(select([SSOModels.permission.c.name]).select_from(join).where(
            SSOModels.user.c.user_id == request["user_id"]))
        permissions = []
        async for perm in select_permissions:
            permissions.append(perm.name)
        return permissions


async def get_user(username):
    async with Connection() as conn:
        select_user = await conn.execute(SSOModels.user.select().where(SSOModels.user.c.username == username))
        user = await select_user.fetchone()
        return user


async def create_and_get_user(username, password):
    async with Connection() as conn:
        insert_user = await conn.execute(SSOModels.user.insert().values(username=username,
                                                                        password=bcrypt.hash(password)))
        user = await insert_user.fetchone()
        return user


async def create_user_group(user_id, group_id):
    async with Connection() as conn:
        await conn.execute(SSOModels.user_group.insert().values(user_id=user_id, group_id=group_id))


async def update_and_get_session(user_id):
    async with Connection() as conn:
        await conn.execute(SSOModels.session.delete().where(SSOModels.session.c.user_id == user_id))
        session_id = str(uuid.uuid4())
        await conn.execute(SSOModels.session.insert().values(session_id=session_id, user_id=user_id))
        return session_id


async def do_sign_out(user_id):
    async with Connection() as conn:
        await conn.execute(SSOModels.session.delete().where(SSOModels.session.c.user_id == user_id))


async def update_password(username, new_password):
    async with Connection() as conn:
        await conn.execute(SSOModels.user.update().where(
            SSOModels.user.c.username == username).values(
            password=bcrypt.hash(new_password)))


def join_user_permission():
    # Return a Join from this FromClause to another FromClause.
    join = SSOModels.user \
        .join(SSOModels.user_group, SSOModels.user.c.user_id == SSOModels.user_group.c.user_id) \
        .join(SSOModels.group, SSOModels.user_group.c.group_id == SSOModels.group.c.group_id) \
        .join(SSOModels.group_permission, SSOModels.group.c.group_id == SSOModels.group_permission.c.group_id) \
        .join(SSOModels.permission, SSOModels.group_permission.c.permission_id == SSOModels.permission.c.permission_id)
    return join
