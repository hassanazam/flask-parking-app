from flask import jsonify
from flask_jwt import jwt_required

from app import app
from app.controllers.admin.booking_details import BookingDetailsController
from app.controllers.admin.view_users_data import UserDataController
from app.services.utils import decorator_utility
from app.services.utils.constants_utility import ConstantsUtility
from app.services.utils.response_utility import Response, ResponseInfo
from app.services.utils.security_utility import SecurityUtility


@app.route("/admin/bookings", methods=["GET"])
@jwt_required()
@SecurityUtility.role_based_access([ConstantsUtility.ADMIN])
@decorator_utility.api_response_handler
def get_booking_details():

    bookings = BookingDetailsController.get_booking_details()

    response = Response(ResponseInfo.CODE_SUCCESS, ResponseInfo.MESSAGE_SUCCESS, data=bookings)
    return jsonify(response.to_dict())


@app.route("/admin/users", methods=["GET"])
@jwt_required()
@SecurityUtility.role_based_access([ConstantsUtility.ADMIN])
@decorator_utility.api_response_handler
def get_users_data():

    users = UserDataController.view_users_data()

    response = Response(ResponseInfo.CODE_SUCCESS, ResponseInfo.MESSAGE_SUCCESS, data=users)
    return jsonify(response.to_dict())
