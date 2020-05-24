from app.services.utils.constants_utility import ConstantsUtility


class Response(object):

    def __init__(self, status_code, message, data=None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def to_dict(self):
        response_dict = {
            ConstantsUtility.STATUS_CODE: self.status_code,
            ConstantsUtility.MESSAGE: self.message
        }

        if self.data:
            response_dict.update({
                ConstantsUtility.DATA: self.data
            })

        return response_dict


class ResponseInfo(object):

    CODE_GENERAL_ERROR = 100
    MESSAGE_GENERAL_ERROR = "General error!"

    CODE_EMAIL_ALREADY_IN_USE = 101
    MESSAGE_EMAIL_ALREADY_IN_USE = "This email is already in use."

    CODE_SUCCESS = 0
    MESSAGE_SUCCESS = "Success"

    CODE_BAD_REQUEST = 400

    CODE_INVALID_AREA_ID = 102
    MESSAGE_INVALID_AREA_ID = "Invalid area id"

    CODE_PARKING_SLOT_ALREADY_BOOKED = 103
    MESSAGE_PARKING_SLOT_ALREADY_BOOKED = "This slot is already booked for the given time."

    MESSAGE_UNAUTHORIZED_ACCESS = "Unauthorized access"
    CODE_UNAUTHORIZED_ACCESS = 401

    CODE_INVALID_SLOT_ID = 103
    MESSAGE_INVALID_SLOT_ID = "Invalid slot id"

    CODE_INVALID_BOOKING_ID = 104
    MESSAGE_INVALID_BOOKING_ID = "Invalid booking id"

    MESSAGE_BOOKING_CANCELLED = "Your booking has been cancelled."

    CODE_INVALID_PARKING_DATE_TIME = 105
    MESSAGE_START_TIME_LESS_THAN_CURRENT_TIME = "Parking start time cannot be less than current time!"
    MESSAGE_END_TIME_LESS_THAN_CURRENT_TIME = "Parking end time cannot be less than current time!"