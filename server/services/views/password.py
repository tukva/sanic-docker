from sanic.exceptions import abort
from marshmallow.exceptions import ValidationError

from services.decorators import authorized
from engine import Connection
from services.forms import ResetPasswordSchema, PasswordMatchError
from services.utils import do_reset_password


@authorized()
async def reset_password(request):
    try:
        data = ResetPasswordSchema().load(request.form)
    except ValidationError as e:
        abort(400, message=e)
    except PasswordMatchError as e:
        abort(423, message=e)
    else:
        async with Connection() as conn:
            return await do_reset_password(conn, data)
