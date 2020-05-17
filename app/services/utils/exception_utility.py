from app.services.utils.response_utility import ResponseInfo


class APIException(Exception):

    def __init__(self, status_code=ResponseInfo.CODE_GENERAL_ERROR, message=ResponseInfo.MESSAGE_GENERAL_ERROR, data=None):
        self.status_code = status_code
        self.message = message
        self.data = data