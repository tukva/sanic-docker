from sanic import Sanic

from config import SSO_API_PORT
from routes import add_routes

app = Sanic(name=__name__)
add_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SSO_API_PORT)
