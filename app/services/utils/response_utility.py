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
