from http import HTTPStatus

import pytest


@pytest.mark.SSO
@pytest.mark.auth
@pytest.mark.sign_up
async def test_sign_up(test_cli, tables):
    resp = await test_cli.post('/sign-up', json={"username": "test_data",
                                                 "password": "test_data",
                                                 "password_repeat": "test_data"})
    assert resp.status == HTTPStatus.OK
    assert await resp.json() == "Ok"

    resp = await test_cli.post('/sign-up', json={"username": "test_data",
                                                 "password": "test_data",
                                                 "password_repeat": "test_data"})
    assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert await resp.json() == "Username already exists"

    resp = await test_cli.post('/sign-up', json={"wrong_test_key": "test_data_2",
                                                 "password": "test_data_2",
                                                 "password_repeat": "test_data_2"})
    assert resp.status == HTTPStatus.BAD_REQUEST

    resp = await test_cli.post('/sign-up', json={"username": "test_data_3",
                                                 "password": "test_data_3",
                                                 "password_repeat": "wrong_test_data_3"})
    assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert await resp.json() == ["Passwords don\'t match"]


@pytest.mark.SSO
@pytest.mark.auth
@pytest.mark.sign_in
async def test_sign_in(test_cli, add_user):
    resp = await test_cli.post('/sign-in', json={"username": "test_data",
                                                 "password": "test_data"})
    assert resp.status == HTTPStatus.OK
    assert await resp.json() == "Ok"

    resp = await test_cli.post('/sign-in', json={"wrong_test_key": "test_data_2",
                                                 "password": "test_data_2"})
    assert resp.status == HTTPStatus.BAD_REQUEST

    resp = await test_cli.post('/sign-in', json={"username": "wrong_test_data",
                                                 "password": "test_data_3"})
    assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert await resp.json() == "Wrong username"

    resp = await test_cli.post('/sign-in', json={"username": "test_data",
                                                 "password": "wrong_test_data"})
    assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert await resp.json() == "Wrong password"


@pytest.mark.SSO
@pytest.mark.auth
@pytest.mark.sign_out
async def test_sign_out(test_cli, add_session):
    resp = await test_cli.post('/sign-out', cookies={"session": add_session})
    assert resp.status == HTTPStatus.OK
    assert await resp.json() == "Ok"

    resp = await test_cli.post('/sign-out')
    assert resp.status == HTTPStatus.UNAUTHORIZED
    assert await resp.json() == {"Status": "Not_authorized"}
