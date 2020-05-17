from cerberus import Validator


class APIValidator(object):

    register_user_validator = {
        "email": {"type": "string", "required": True},
        "password": {"type": "string", "required": True}
    }

    def validate_register_user_api(data):
        vf = Validator(APIValidator.register_user_validator)
        return vf.validate(data), APIValidator.register_user_validator
