from cerberus import Validator


class APIValidator(object):

    register_user_validator = {
        "email": {"type": "string", "required": True},
        "password": {"type": "string", "required": True}
    }

    create_parking_area_validator = {
        "name": {"type": "string", "required": True},
        "image": {"type": "string", "required": False}
    }

    create_parking_slot_validator = {
        "parking_area_id": {"type": "integer", "required": True},
    }

    book_parking_slot_validator = {
        "parking_slot_id": {"type": "integer", "required": True},
        "start_time": {"type": "integer", "required": True},
        "end_time": {"type": "integer", "required": True}
    }

    cancel_parking_slot_booking_validator = {
        "booking_id": {"type": "integer", "required": True},
    }

    @staticmethod
    def validate_register_user_api(data):
        vf = Validator(APIValidator.register_user_validator)
        return vf.validate(data), APIValidator.register_user_validator

    @staticmethod
    def validate_create_parking_area_api(data):
        vf = Validator(APIValidator.create_parking_area_validator)
        return vf.validate(data), APIValidator.create_parking_area_validator

    @staticmethod
    def validate_create_parking_slot_api(data):
        vf = Validator(APIValidator.create_parking_slot_validator)
        return vf.validate(data), APIValidator.create_parking_slot_validator

    @staticmethod
    def validate_book_parking_slot_api(data):
        vf = Validator(APIValidator.book_parking_slot_validator)
        return vf.validate(data), APIValidator.book_parking_slot_validator

    @staticmethod
    def validate_cancel_parking_slot_booking_api(data):
        vf = Validator(APIValidator.cancel_parking_slot_booking_validator)
        return vf.validate(data), APIValidator.cancel_parking_slot_booking_validator



