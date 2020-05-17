from flask import jsonify

from app import app
from app.controllers.user import UserController
from app.services.utils import decorator_utility
from app.services.utils.common_utility import CommonUtility
from app.services.utils.response_utility import Response, ResponseInfo
from app.services.utils.validation_utils import APIValidator


@app.route("/user/register", methods=["POST"])
@decorator_utility.api_response_handler
def register_user():
    """
    Required parameters :
    email, password
    :return:
    """

    data = CommonUtility.get_request_data()
    valid, schema = APIValidator.validate_register_user_api(data)
    if not valid:
        return schema, 400

    email = data["email"]
    password = data["password"]

    user = UserController.register_user(email, password)

    if user:
        response = Response(ResponseInfo.CODE_SUCCESS, ResponseInfo.MESSAGE_SUCCESS)
        return jsonify(response.to_dict())
