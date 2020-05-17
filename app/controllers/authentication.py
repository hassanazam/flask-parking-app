"""
Author: Hassan Azam
Description : This file contains AuthenticationController. It encapsulates the logic of authenticating a user.
"""
from app.services.utils.security_utility import SecurityUtility
from app.services.utils.user_utility import UserUtility

# Initialize Flask JWT instance
from flask_jwt import JWT


class AuthenticationController(object):

    @staticmethod
    def authenticate(email, password):
        user = UserUtility.get_user_by_email(email, return_as_dict=False)
        if user and SecurityUtility.verify_password(password, user.password):
            return user

    @staticmethod
    def get_authenticated_user(payload):
        user_id = payload['identity']
        return UserUtility.get_user_by_id(user_id)


from app import app

jwt = JWT(app, AuthenticationController.authenticate, AuthenticationController.get_authenticated_user)
