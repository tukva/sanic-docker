from marshmallow import Schema, fields, validate


class SignupSchema(Schema):
    username = fields.Str(
        validate=validate.Length(min=4, max=40), required=True, nullable=False
    )
    password = fields.Str(
        validate=validate.Length(min=6, max=255), required=True, nullable=False, load_only=True
    )
    password_repeat = fields.Str(
        validate=validate.Length(min=6, max=255), required=True, nullable=False, load_only=True
    )


class SigninSchema(Schema):
    username = fields.Str(
        validate=validate.Length(min=4, max=40), required=True, nullable=False
    )
    password = fields.Str(
        validate=validate.Length(min=6, max=255), required=True, nullable=False, load_only=True
    )


class ResetPasswordSchema(Schema):
    username = fields.Str(
        validate=validate.Length(min=4, max=40), required=True, nullable=False
    )
    old_password = fields.Str(
        validate=validate.Length(min=6, max=255), required=True, nullable=False, load_only=True
    )
    new_password = fields.Str(
        validate=validate.Length(min=6, max=255), required=True, nullable=False, load_only=True
    )
    new_password_repeat = fields.Str(
        validate=validate.Length(min=6, max=255), required=True, nullable=False, load_only=True
    )
