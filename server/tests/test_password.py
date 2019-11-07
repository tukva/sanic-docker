import pytest


@pytest.mark.SSO
@pytest.mark.password
@pytest.mark.reset_password
async def test_reset_password(test_cli, add_session):
    resp = await test_cli.patch('/reset-password',
                                data={"username": "test_data",
                                      "old_password": "test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == 401
    assert await resp.text() == '{"Status":"Not_authorized"}'

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                data={"username": "test_data",
                                      "old_password": "test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == 200
    assert await resp.text() == "Ok"

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                data={"username": "wrong_test_data",
                                      "old_password": "test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == 423
    assert await resp.text() == "Wrong username"

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                data={"username": "test_data",
                                      "old_password": "wrong_test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == 423
    assert await resp.text() == "Wrong old password"

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                data={"username": "test_data",
                                      "old_password": "new_test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "test_data"})
    assert resp.status == 423
    assert await resp.text() == "Error: New passwords don\'t match"
