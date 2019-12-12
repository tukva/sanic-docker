from http import HTTPStatus

import pytest


@pytest.mark.SSO
@pytest.mark.reset_password
async def test_reset_password(test_cli, add_session):
    resp = await test_cli.patch('/reset-password',
                                json={"username": "test_data",
                                      "old_password": "test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == HTTPStatus.UNAUTHORIZED
    assert await resp.json() == {"Status": "Not_authorized"}

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                json={"username": "test_data",
                                      "old_password": "test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == HTTPStatus.OK
    assert await resp.json() == "Ok"

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                json={"username": "wrong_test_data",
                                      "old_password": "test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert await resp.json() == "Wrong username"

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                json={"username": "test_data",
                                      "old_password": "wrong_test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert await resp.json() == "Wrong old password"

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                json={"username": "test_data",
                                      "old_password": "new_test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "test_data"})
    assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert await resp.json() == ["New passwords don\'t match"]
