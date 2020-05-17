from flask import jsonify
from flask_jwt import jwt_required

from app import app
from app.controllers.parking_area import ParkingAreaController
from app.controllers.parking_slot import ParkingSlotController
from app.services.utils import decorator_utility
from app.services.utils.common_utility import CommonUtility
from app.services.utils.constants_utility import ConstantsUtility
from app.services.utils.response_utility import Response, ResponseInfo
from app.services.utils.security_utility import SecurityUtility
from app.services.utils.validation_utils import APIValidator


@app.route("/parking-slot", methods=["POST"], endpoint='create_parking_slot')
@jwt_required()
@SecurityUtility.role_based_access([ConstantsUtility.ADMIN])
@decorator_utility.api_response_handler
def create_parking_slot_api():
    """
    Create a new parking area
    :return:
    """

    data = CommonUtility.get_request_data()
    valid, schema = APIValidator.validate_create_parking_slot_api(data)
    if not valid:
        return schema, ResponseInfo.CODE_BAD_REQUEST

    parking_area_id = data["parking_area_id"]

    parking_slot = ParkingSlotController.create_parking_slot(parking_area_id)

    if parking_slot:
        data = {
            ConstantsUtility.PARKING_SLOT: parking_slot
        }
        response = Response(ResponseInfo.CODE_SUCCESS, ResponseInfo.MESSAGE_SUCCESS, data=data)
        return jsonify(response.to_dict())


@app.route("/parking-slot/book", methods=["POST"], endpoint='book_parking_slot')
@jwt_required()
@SecurityUtility.role_based_access([ConstantsUtility.CUSTOMER])
@decorator_utility.api_response_handler
def book_parking_slot_api():
    """
    Book a parking slot
    :return:
    """

    data = CommonUtility.get_request_data()
    valid, schema = APIValidator.validate_book_parking_slot_api(data)
    if not valid:
        return schema, ResponseInfo.CODE_BAD_REQUEST

    parking_slot_id = data[ConstantsUtility.PARKING_SLOT_ID]
    start_time = data[ConstantsUtility.START_TIME]
    end_time = data[ConstantsUtility.END_TIME]

    booking_details = ParkingSlotController.book_parking_slot(parking_slot_id, start_time, end_time)

    if booking_details:
        data = {
            ConstantsUtility.BOOKING_DETAILS: booking_details
        }
        response = Response(ResponseInfo.CODE_SUCCESS, ResponseInfo.MESSAGE_SUCCESS, data=data)
        return jsonify(response.to_dict())



@app.route("/parking-slot/cancel-booking", methods=["POST"], endpoint='cancel_parking_slot_booking')
@jwt_required()
@SecurityUtility.role_based_access([ConstantsUtility.CUSTOMER, ConstantsUtility.ADMIN])
@decorator_utility.api_response_handler
def cancel_parking_slot_booking_api():
    """
    Cancel a parking slot booking
    :return:
    """

    data = CommonUtility.get_request_data()
    valid, schema = APIValidator.validate_cancel_parking_slot_booking_api(data)
    if not valid:
        return schema, ResponseInfo.CODE_BAD_REQUEST

    booking_id = data["booking_id"]

    cancelled = ParkingSlotController.cancel_parking_slot_booking(booking_id)


    response = Response(ResponseInfo.CODE_SUCCESS, ResponseInfo.MESSAGE_BOOKING_CANCELLED)
    return jsonify(response.to_dict())
