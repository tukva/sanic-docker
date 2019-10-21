from marshmallow import Schema, fields, validate


class SignupRequestSchema(Schema):
    username = fields.Str(
        validate=validate.Length(max=40), required=True
    )
    password = fields.Str(
        validate=validate.Length(max=255), required=True
    )
    password_repeat = fields.Str(
        validate=validate.Length(max=255), required=True
    )


class SigninRequestSchema(Schema):
    username = fields.Str(
        validate=validate.Length(max=40), required=True
    )
    password = fields.Str(
        validate=validate.Length(max=255), required=True
    )


class ResetPasswordRequestSchema(Schema):
    username = fields.Str(
        validate=validate.Length(max=40), required=True
    )
    old_password = fields.Str(
        validate=validate.Length(max=255), required=True
    )
    new_password = fields.Str(
        validate=validate.Length(max=255), required=True
    )
    new_password_repeat = fields.Str(
        validate=validate.Length(max=255), required=True
    )


class PermitEditRequestSchema(Schema):
    user_id = fields.Int(required=True)
