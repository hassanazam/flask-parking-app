from app import db
from app.models.role import Role
from app.models.user import User
from app.services.utils.constants_utility import ConstantsUtility
from app.services.utils.security_utility import SecurityUtility


class UserUtility(object):

    @staticmethod
    def create_user(email, password):

        password_hash = SecurityUtility.generate_password_hash(password)

        role = Role.query.filter_by(name=ConstantsUtility.CUSTOMER).first()
        user = User(email=email, password=password_hash, role=role)

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
        user = User.query.filter_by(id=id).first()
        if user:
            return user

    @staticmethod
    def create_admin(email, password):

        password_hash = SecurityUtility.generate_password_hash(password)

        role = Role.query.filter_by(name=ConstantsUtility.ADMIN).first()
        user = User(email=email, password=password_hash, role=role)

        db.session.add(user)
        db.session.commit()

        return user
