from http import HTTPStatus

from passlib.hash import bcrypt
from sanic.response import json
from marshmallow.exceptions import ValidationError

from services.decorators import authorized
from services.forms import ResetPasswordSchema, PasswordMatchError
from services.utils import get_user, update_password


@authorized()
async def reset_password(request):
    try:
        data = ResetPasswordSchema().load(request.json)
    except ValidationError as e:
        return json(e.messages, HTTPStatus.BAD_REQUEST)
    except PasswordMatchError as e:
        return json(e.args, HTTPStatus.UNPROCESSABLE_ENTITY)

    user = await get_user(data["username"])

    if not user:
        return json("Wrong username", HTTPStatus.UNPROCESSABLE_ENTITY)
    if not bcrypt.verify(data["old_password"], user.password):
        return json("Wrong old password", HTTPStatus.UNPROCESSABLE_ENTITY)

    await update_password(data["username"], data["new_password"])

    return json("Ok", HTTPStatus.OK)
