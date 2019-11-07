import pytest


@pytest.mark.SSO
@pytest.mark.auth
@pytest.mark.sign_up
async def test_sign_up(test_cli, tables):
    resp = await test_cli.post('/sign-up', data={"username": "test_data",
                                                 "password": "test_data",
                                                 "password_repeat": "test_data"})
    assert resp.status == 200
    assert await resp.text() == "Ok"

    resp = await test_cli.post('/sign-up', data={"username": "test_data",
                                                 "password": "test_data",
                                                 "password_repeat": "test_data"})
    assert resp.status == 423
    assert await resp.text() == "Username already exists"

    resp = await test_cli.post('/sign-up', data={"wrong_test_key": "test_data_2",
                                                 "password": "test_data_2",
                                                 "password_repeat": "test_data_2"})
    assert resp.status == 400

    resp = await test_cli.post('/sign-up', data={"username": "test_data_3",
                                                 "password": "test_data_3",
                                                 "password_repeat": "wrong_test_data_3"})
    assert resp.status == 423
    assert await resp.text() == "Error: Passwords don\'t match"


@pytest.mark.SSO
@pytest.mark.auth
@pytest.mark.sign_in
async def test_sign_in(test_cli, add_user):
    resp = await test_cli.post('/sign-in', data={"username": "test_data",
                                                 "password": "test_data"})
    assert resp.status == 200
    assert await resp.text() == "Ok"

    resp = await test_cli.post('/sign-in', data={"wrong_test_key": "test_data_2",
                                                 "password": "test_data_2"})
    assert resp.status == 400

    resp = await test_cli.post('/sign-in', data={"username": "wrong_test_data",
                                                 "password": "test_data_3"})
    assert resp.status == 423
    assert await resp.text() == "Wrong username"

    resp = await test_cli.post('/sign-in', data={"username": "test_data",
                                                 "password": "wrong_test_data"})
    assert resp.status == 423
    assert await resp.text() == "Wrong password"


@pytest.mark.SSO
@pytest.mark.auth
@pytest.mark.sign_out
async def test_sign_out(test_cli, add_session):
    resp = await test_cli.post('/sign-out', cookies={"session": add_session})
    assert resp.status == 200
    assert await resp.text() == "Ok"

    resp = await test_cli.post('/sign-out')
    assert resp.status == 401
    assert await resp.text() == '{"Status":"Not_authorized"}'
