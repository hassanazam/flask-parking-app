from app.services.utils.exception_utility import APIException
from app.services.utils.response_utility import ResponseInfo
from app.services.utils.user_utility import UserUtility


class UserController(object):

    @staticmethod
    def register_user(email, password):

        # Check if email already exists
        user = UserUtility.get_user_by_email(email)
        if user:
            raise APIException(status_code=ResponseInfo.CODE_EMAIL_ALREADY_IN_USE,
                               message=ResponseInfo.MESSAGE_EMAIL_ALREADY_IN_USE)

        user = UserUtility.create_user(email, password)
        return user
