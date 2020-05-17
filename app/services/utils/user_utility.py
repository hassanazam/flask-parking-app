from app import db
from app.models.user import User
from app.services.utils.security_utility import SecurityUtility


class UserUtility(object):

    @staticmethod
    def create_user(email, password):

        password_hash = SecurityUtility.generate_password_hash(password)

        user = User(email=email, password=password_hash)

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def get_user_by_email(email, return_as_dict=True):
        user = User.query.filter_by(email=email).first()
        if user:
            return user.__dict__ if return_as_dict else user

    @staticmethod
    def get_user_by_id(id):
        user = User.query.filter_by(id=id)
        if user:
            return user.__dict__
