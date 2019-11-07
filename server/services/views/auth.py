from sanic.exceptions import abort
from marshmallow.exceptions import ValidationError

from services.decorators import authorized
from services.forms import SignupSchema, SigninSchema, PasswordMatchError
from engine import Connection
from services.utils import do_sign_up, do_sign_in, do_sign_out


async def sign_up(request):
    try:
        data = SignupSchema().load(request.form)
    except ValidationError as e:
        abort(400, message=e)
    except PasswordMatchError as e:
        abort(423, message=e)
    else:
        async with Connection() as conn:
            return await do_sign_up(conn, data)


async def sign_in(request):
    try:
        data = SigninSchema().load(request.form)
    except ValidationError as e:
        abort(400, message=e)
    else:
        async with Connection() as conn:
            return await do_sign_in(conn, data)


@authorized()
async def sign_out(request):
    async with Connection() as conn:
        return await do_sign_out(request, conn)
