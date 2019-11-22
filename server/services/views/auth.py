from sanic.response import json
from sanic.log import logger
from marshmallow.exceptions import ValidationError

from services.decorators import authorized
from services.forms import SignupSchema, SigninSchema, PasswordMatchError
from engine import Connection
from services.utils import do_sign_up, do_sign_in, do_sign_out


async def sign_up(request):
    try:
        data = SignupSchema().load(request.json)
    except ValidationError as e:
        logger.error(e)
        return json(e.messages, 400)
    except PasswordMatchError as e:
        logger.error(e)
        return json(e.args, 423)
    async with Connection() as conn:
        return await do_sign_up(conn, data)


async def sign_in(request):
    try:
        data = SigninSchema().load(request.json)
    except ValidationError as e:
        logger.error(e.messages)
        return json(e, 400)
    async with Connection() as conn:
        return await do_sign_in(conn, data)


@authorized()
async def sign_out(request):
    async with Connection() as conn:
        return await do_sign_out(request, conn)
