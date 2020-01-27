from http import HTTPStatus

import psycopg2
from passlib.hash import bcrypt
from sanic.response import json
from sanic.log import logger
from marshmallow.exceptions import ValidationError

from constants import Group
from services.decorators import authorized
from services.forms import SignupSchema, SigninSchema, PasswordMatchError
from services.utils import create_and_get_user, create_user_group, get_user, update_and_get_session, do_sign_out


async def sign_up(request):
    try:
        data = SignupSchema().load(request.json)
    except ValidationError as e:
        logger.error(e)
        return json(e.messages, HTTPStatus.BAD_REQUEST)
    except PasswordMatchError as e:
        logger.error(e)
        return json(e.args, HTTPStatus.UNPROCESSABLE_ENTITY)

    try:
        user = await create_and_get_user(data["username"], data["password"])
    except psycopg2.IntegrityError as e:
        logger.error(e)
        return json("Username already exists", HTTPStatus.UNPROCESSABLE_ENTITY)

    await create_user_group(user.user_id, Group.VIEWER)
    return json("Ok", HTTPStatus.OK)


async def sign_in(request):
    try:
        data = SigninSchema().load(request.json)
    except ValidationError as e:
        logger.error(e.messages)
        return json(e, HTTPStatus.BAD_REQUEST)

    user = await get_user(data["username"])

    if not user:
        return json("Wrong username", HTTPStatus.UNPROCESSABLE_ENTITY)
    if not bcrypt.verify(data["password"], user.password):
        return json("Wrong password", HTTPStatus.UNPROCESSABLE_ENTITY)

    session_id = await update_and_get_session(user.user_id)

    response = json("Ok", HTTPStatus.OK)
    response.cookies['session'] = session_id
    return response


@authorized()
async def sign_out(request):
    user_id = request.get("user_id")
    await do_sign_out(user_id)
    return json("Ok", HTTPStatus.OK)
