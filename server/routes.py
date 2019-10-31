from listeners import acquire_con, close_con
from services.views.auth import sign_up, sign_in, sign_out
from services.views.password import reset_password


def add_routes(app):
    app.register_listener(acquire_con, "before_server_start")
    app.register_listener(close_con, "after_server_stop")

    app.add_route(sign_up, '/sign-up', methods=['POST'])
    app.add_route(sign_in, '/sign-in', methods=['POST'])
    app.add_route(sign_out, '/sign-out', methods=['POST'])

    app.add_route(reset_password, '/reset-password', methods=["PATCH"])
