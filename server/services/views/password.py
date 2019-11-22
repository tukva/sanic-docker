from sanic.response import json
from marshmallow.exceptions import ValidationError

from services.decorators import authorized
from engine import Connection
from services.forms import ResetPasswordSchema, PasswordMatchError
from services.utils import do_reset_password


@authorized()
async def reset_password(request):
    try:
        data = ResetPasswordSchema().load(request.json)
    except ValidationError as e:
        return json(e.messages, 400)
    except PasswordMatchError as e:
        return json(e.args, 423)
    async with Connection() as conn:
        return await do_reset_password(conn, data)
