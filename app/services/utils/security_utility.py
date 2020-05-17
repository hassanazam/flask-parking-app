from functools import wraps

from flask_jwt import current_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app.services.utils.common_utility import CommonUtility
from app.services.utils.constants_utility import ConstantsUtility
from app.services.utils.response_utility import ResponseInfo


class SecurityUtility(object):

    def generate_password_hash(password):
        return generate_password_hash(password)

    def verify_password(password, password_hash):
        return check_password_hash(password_hash, password)

    # A decorator for implementing role based access on APIs
    def role_based_access(allowed_roles):
        """Ensures that only the given roles are allowed to access the route."""

        def decorator(view_function):
            """First level decorator"""

            @wraps(view_function)
            def role_wrapper(*args, **kwargs):
                """Wraps the view function"""

                # Get authenticated user
                user = CommonUtility.get_authenticated_user()

                if user.role.name not in allowed_roles:
                    return ResponseInfo.MESSAGE_UNAUTHORIZED_ACCESS, ResponseInfo.CODE_UNAUTHORIZED_ACCESS

                return view_function(*args, **kwargs)

            return role_wrapper

        return decorator
