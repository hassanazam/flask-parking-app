from flask import jsonify
from flask_jwt import jwt_required

from app import app
from app.controllers.parking_area import ParkingAreaController
from app.services.utils import decorator_utility
from app.services.utils.common_utility import CommonUtility
from app.services.utils.constants_utility import ConstantsUtility
from app.services.utils.response_utility import Response, ResponseInfo
from app.services.utils.security_utility import SecurityUtility
from app.services.utils.validation_utils import APIValidator


@app.route("/parking-area", methods=["POST"])
@jwt_required()
@SecurityUtility.role_based_access([ConstantsUtility.ADMIN])
@decorator_utility.api_response_handler
def create_parking_area_api():
    """
    Create a new parking area
    :return:
    """

    data = CommonUtility.get_request_data()
    valid, schema = APIValidator.validate_create_parking_area_api(data)
    if not valid:
        return schema, 400

    name = data["name"]
    image = data.get("image")

    parking_area = ParkingAreaController.create_parking_area(name, image)

    if parking_area:
        data = {
            ConstantsUtility.PARKING_AREA: parking_area
        }
        response = Response(ResponseInfo.CODE_SUCCESS, ResponseInfo.MESSAGE_SUCCESS, data=data)
        return jsonify(response.to_dict())


@app.route("/parking-areas", methods=["GET"], endpoint='get_parking_areas')
@jwt_required()
@SecurityUtility.role_based_access([ConstantsUtility.ADMIN, ConstantsUtility.CUSTOMER])
@decorator_utility.api_response_handler
def get_parking_areas_api():
    """
    List all parking areas
    :return:
    """

    parking_areas = ParkingAreaController.list_parking_areas()

    data = {
        ConstantsUtility.PARKING_AREAS: parking_areas if parking_areas else []
    }
    response = Response(ResponseInfo.CODE_SUCCESS, ResponseInfo.MESSAGE_SUCCESS, data=data)
    return jsonify(response.to_dict())


@app.route("/parking-area/<area_id>/slots", methods=["GET"], endpoint='get_parking_area_slots')
@jwt_required()
@SecurityUtility.role_based_access([ConstantsUtility.ADMIN, ConstantsUtility.CUSTOMER])
@decorator_utility.api_response_handler
def get_parking_area_slots_api(area_id):
    """
    List all parking areas
    :return:
    """

    if not area_id:
        return ResponseInfo.MESSAGE_INVALID_AREA_ID, ResponseInfo.CODE_BAD_REQUEST

    parking_slots = ParkingAreaController.list_slots_of_parking_area(area_id)

    data = {
        ConstantsUtility.PARKING_SLOTS: parking_slots if parking_slots else []
    }
    response = Response(ResponseInfo.CODE_SUCCESS, ResponseInfo.MESSAGE_SUCCESS, data=data)
    return jsonify(response.to_dict())
