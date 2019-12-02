from listeners import acquire_con, close_con
from services.views.auth import sign_up, sign_in, sign_out
from services.views.password import reset_password
from services.views.check_access import check_auth, check_auth_and_user_has, \
    check_auth_and_user_in_group, check_auth_and_get_user_permissions


def add_routes(app):
    app.register_listener(acquire_con, "before_server_start")
    app.register_listener(close_con, "after_server_stop")

    app.add_route(sign_up, '/sign-up', methods=['POST'])
    app.add_route(sign_in, '/sign-in', methods=['POST'])
    app.add_route(sign_out, '/sign-out', methods=['POST'])

    app.add_route(reset_password, '/reset-password', methods=["PATCH"])

    app.add_route(check_auth, '/check-auth', methods=["POST"])
    app.add_route(check_auth_and_user_has, '/check-permission', methods=["POST"])
    app.add_route(check_auth_and_user_in_group, '/check-group', methods=["POST"])
    app.add_route(check_auth_and_get_user_permissions, '/get-permissions', methods=["POST"])
