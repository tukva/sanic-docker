from sanic import Sanic

from views.auth import sign_up, sign_in, sign_out
from listener import prepare_db
from views.password import reset_password


app = Sanic(name=__name__)

app.register_listener(prepare_db, "before_server_start")

app.add_route(sign_up, '/sign-up', methods=['POST'])
app.add_route(sign_in, '/sign-in', methods=['POST'])
app.add_route(sign_out, '/sign-out', methods=['POST'])

app.add_route(reset_password, '/reset-password', methods=["PATCH"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
