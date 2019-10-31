import pytest
from sanic import Sanic
from passlib.hash import bcrypt
from sqlalchemy.schema import CreateTable, DropTable

from routes import add_routes
from engine import Connection, Engine
from models import tb_group_permission, tb_user_group, tb_user, tb_group, tb_session, tb_permission
from services.utils import generate_session_id


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
        await conn.execute(DropTable(tb_group_permission))
        await conn.execute(DropTable(tb_user_group))
        await conn.execute(DropTable(tb_user))
        await conn.execute(DropTable(tb_group))
        await conn.execute(DropTable(tb_session))
        await conn.execute(DropTable(tb_permission))
        assert True


async def create_tables():
    async with Connection() as conn:
        await conn.execute(CreateTable(tb_user))
        await conn.execute(CreateTable(tb_group))
        await conn.execute(CreateTable(tb_session))
        await conn.execute(CreateTable(tb_permission))
        await conn.execute(CreateTable(tb_group_permission))
        await conn.execute(CreateTable(tb_user_group))
        await conn.execute(tb_group.insert().values(group_id=1, name="admins"))
        await conn.execute(tb_group.insert().values(group_id=2, name="viewers"))
        await conn.execute(tb_group.insert().values(group_id=3, name="editors"))
        await conn.execute(tb_permission.insert().values(permission_id=1, name="special"))
        await conn.execute(tb_permission.insert().values(permission_id=2, name="view"))
        await conn.execute(tb_permission.insert().values(permission_id=3, name="edit"))
        await conn.execute(tb_group_permission.insert().values(permission_id=1, group_id=1))
        await conn.execute(tb_group_permission.insert().values(permission_id=1, group_id=2))
        await conn.execute(tb_group_permission.insert().values(permission_id=1, group_id=3))
        await conn.execute(tb_group_permission.insert().values(permission_id=2, group_id=2))
        await conn.execute(tb_group_permission.insert().values(permission_id=2, group_id=3))
        assert True


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
        await conn.execute(tb_user.insert().values(username="test_data", password=bcrypt.hash("test_data")))


@pytest.fixture
async def add_session(add_user):
    async with Connection() as conn:
        session_id = generate_session_id()
        await conn.execute(tb_session.insert().values(session_id=session_id, user_id=1))
        return session_id


@pytest.fixture
async def connection():
    await Engine.init()

    yield

    await Engine.close()
