import uuid

import pytest
from sanic import Sanic
from passlib.hash import bcrypt
from sqlalchemy.schema import CreateTable, DropTable

from routes import add_routes
from engine import Connection, Engine
from models import _SSO as SSO


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "SSO: SSO tests")
    config.addinivalue_line("markers", "auth: auth tests")
    config.addinivalue_line("markers", "password: password tests")
    config.addinivalue_line("markers", "sign_in: sign_in test")
    config.addinivalue_line("markers", "sign_up: sign_up test")
    config.addinivalue_line("markers", "sign_out: sign_out test")
    config.addinivalue_line("markers", "reset_password: reset_password test")


async def drop_tables():
    async with Connection() as conn:
        await conn.execute(DropTable(SSO.group_permission))
        await conn.execute(DropTable(SSO.user_group))
        await conn.execute(DropTable(SSO.user))
        await conn.execute(DropTable(SSO.group))
        await conn.execute(DropTable(SSO.session))
        await conn.execute(DropTable(SSO.permission))


async def create_tables():
    async with Connection() as conn:
        await conn.execute(CreateTable(SSO.user))
        await conn.execute(CreateTable(SSO.group))
        await conn.execute(CreateTable(SSO.session))
        await conn.execute(CreateTable(SSO.permission))
        await conn.execute(CreateTable(SSO.group_permission))
        await conn.execute(CreateTable(SSO.user_group))
        await conn.execute(SSO.group.insert().values(group_id=1, name="admins"))
        await conn.execute(SSO.group.insert().values(group_id=2, name="viewers"))
        await conn.execute(SSO.group.insert().values(group_id=3, name="editors"))
        await conn.execute(SSO.permission.insert().values(permission_id=1, name="special"))
        await conn.execute(SSO.permission.insert().values(permission_id=2, name="view"))
        await conn.execute(SSO.permission.insert().values(permission_id=3, name="edit"))
        await conn.execute(SSO.group_permission.insert().values(permission_id=1, group_id=1))
        await conn.execute(SSO.group_permission.insert().values(permission_id=1, group_id=2))
        await conn.execute(SSO.group_permission.insert().values(permission_id=1, group_id=3))
        await conn.execute(SSO.group_permission.insert().values(permission_id=2, group_id=2))
        await conn.execute(SSO.group_permission.insert().values(permission_id=2, group_id=3))


@pytest.fixture
def test_cli(loop, sanic_client):
    app = Sanic()
    add_routes(app)
    return loop.run_until_complete(sanic_client(app))


@pytest.fixture
async def tables(test_cli):
    await create_tables()

    yield

    await drop_tables()


@pytest.fixture
async def add_user(tables):
    async with Connection() as conn:
        await conn.execute(SSO.user.insert().values(username="test_data", password=bcrypt.hash("test_data")))


@pytest.fixture
async def add_session(add_user):
    async with Connection() as conn:
        session_id = str(uuid.uuid4())
        await conn.execute(SSO.session.insert().values(session_id=session_id, user_id=1))
        return session_id


@pytest.fixture
async def connection():
    await Engine.init()

    yield

    await Engine.close()
