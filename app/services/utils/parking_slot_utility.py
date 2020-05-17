from app import db
from app.models.parking_slot import ParkingSlot
from app.services.utils.booking_utility import BookingUtility
from app.services.utils.common_utility import CommonUtility
from app.services.utils.exception_utility import APIException
from app.services.utils.response_utility import ResponseInfo


class ParkingSlotUtility(object):

    @staticmethod
    def get_all_slots_by_area_id(area_id):

        parking_slots = ParkingSlot.query.filter_by(parking_area_id=area_id).all()

        return CommonUtility.convert_to_dict(parking_slots)


    @staticmethod
    def book_parking_slot(slot_id, start_time, end_time):

        booking = BookingUtility.create_booking(slot_id, start_time, end_time)
        return booking

    @staticmethod
    def mark_parking_slot_as_cancelled():
        pass

    @staticmethod
    def create_parking_slot(area_id):

        slot = ParkingSlot(parking_area_id=area_id)

        db.session.add(slot)
        db.session.commit()

        return CommonUtility.convert_to_dict(slot)

    @staticmethod
    def is_parking_slot_available(parking_slot_id, start_time, end_time):

        booking = BookingUtility.get_booking_by_slot_id_and_time(parking_slot_id, start_time, end_time)
        if booking:
            return False, booking

        return True, None

    @staticmethod
    def validate_parking_slot_id(slot_id):

        slot = ParkingSlotUtility.get_slot_by_id(slot_id)
        if not slot:
            raise APIException(status_code=ResponseInfo.CODE_INVALID_SLOT_ID,
                               message=ResponseInfo.MESSAGE_INVALID_SLOT_ID)

    @staticmethod
    def get_slot_by_id(slot_id):

        slot = ParkingSlot.query.filter_by(id=slot_id).first()
        if slot:
            return CommonUtility.convert_to_dict(slot)

