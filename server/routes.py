from listeners import acquire_con, close_con
from services.views.auth import sign_up, sign_in, sign_out
from services.views.password import reset_password
from services.views.check_access import is_permission_granted, is_group_granted


def add_routes(app):
    app.register_listener(acquire_con, "before_server_start")
    app.register_listener(close_con, "after_server_stop")

    app.add_route(sign_up, '/sign-up', methods=['POST'])
    app.add_route(sign_in, '/sign-in', methods=['POST'])
    app.add_route(sign_out, '/sign-out', methods=['POST'])

    app.add_route(reset_password, '/reset-password', methods=["PATCH"])

    app.add_route(is_permission_granted, '/is-permission-granted', methods=["GET"])
    app.add_route(is_group_granted, '/is-group-granted', methods=["GET"])
