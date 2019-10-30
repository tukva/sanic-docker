async def test_reset_password(test_cli, add_session):
    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                data={"username": "test_data",
                                      "old_password": "test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == 200

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                data={"username": "wrong_test_data",
                                      "old_password": "test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "new_test_data"})
    assert resp.status == 400

    resp = await test_cli.patch('/reset-password', cookies={"session": add_session},
                                data={"username": "test_data",
                                      "old_password": "new_test_data",
                                      "new_password": "new_test_data",
                                      "new_password_repeat": "test_data"})
    assert resp.status == 400
    assert await resp.text() == '"Bad Request. New passwords don\'t match"'
