from marshmallow import Schema, fields, validate, validates_schema


class PasswordMatchError(Exception):
    pass


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

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data["password"] != data["password_repeat"]:
            raise PasswordMatchError("Passwords don't match")


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

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data["new_password"] != data["new_password_repeat"]:
            raise PasswordMatchError("New passwords don't match")
