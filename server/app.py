from sanic import Sanic
from sanic_cors import CORS

from config import SSO_API_PORT, SSO_API_HOST
from routes import add_routes

app = Sanic(name=__name__)
cors = CORS(app, automatic_options=True, supports_credentials=True)
add_routes(app)

if __name__ == '__main__':
    app.run(host=SSO_API_HOST, port=SSO_API_PORT)
