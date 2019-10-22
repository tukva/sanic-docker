from listeners import prepare_db
from services.views.auth import sign_up, sign_in, sign_out
from services.views.password import reset_password
from services.views.admin import permit_edit


def add_routes(app):
    app.register_listener(prepare_db, "before_server_start")

    app.add_route(permit_edit, '/permit-edit', methods=['PATCH'])

    app.add_route(sign_up, '/sign-up', methods=['POST'])
    app.add_route(sign_in, '/sign-in', methods=['POST'])
    app.add_route(sign_out, '/sign-out', methods=['POST'])

    app.add_route(reset_password, '/reset-password', methods=["PATCH"])
