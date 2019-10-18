from sanic import Sanic

from listener import prepare_db
from views.auth import sign_up, sign_in, sign_out
from views.password import reset_password
from views.admin import permit_edit


app = Sanic(name=__name__)

app.register_listener(prepare_db, "before_server_start")

app.add_route(permit_edit, '/permit-edit/users/<user_id>', methods=['PATCH'])

app.add_route(sign_up, '/sign-up', methods=['POST'])
app.add_route(sign_in, '/sign-in', methods=['POST'])
app.add_route(sign_out, '/sign-out', methods=['POST'])

app.add_route(reset_password, '/reset-password', methods=["PATCH"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
