from app.services.utils.booking_utility import BookingUtility
from app.services.utils.common_utility import CommonUtility
from app.services.utils.exception_utility import APIException
from app.services.utils.parking_area_utility import ParkingAreaUtility
from app.services.utils.parking_slot_utility import ParkingSlotUtility
from app.services.utils.response_utility import ResponseInfo


class ParkingSlotController(object):

    @staticmethod
    def create_parking_slot(area_id):

        # Validate area_id
        if not ParkingAreaUtility.get_parking_area_by_id(area_id):
            raise APIException(status_code=ResponseInfo.CODE_INVALID_AREA_ID,
                               message=ResponseInfo.MESSAGE_INVALID_AREA_ID)

        parking_slot = ParkingSlotUtility.create_parking_slot(area_id)

        return parking_slot

    @staticmethod
    def book_parking_slot(parking_slot_id, start_time, end_time):

        # Validate slot id, if not valid then an exception will be raised
        ParkingSlotUtility.validate_parking_slot_id(parking_slot_id)

        # Check if parking slot is available for the requested date time range
        available, booking = ParkingSlotUtility.is_parking_slot_available(parking_slot_id, start_time, end_time)
        if not available:
            raise APIException(status_code=ResponseInfo.CODE_PARKING_SLOT_ALREADY_BOOKED,
                               message=ResponseInfo.MESSAGE_PARKING_SLOT_ALREADY_BOOKED, data={"id": booking.id})

        # Book the slot for the given date time period
        booking = ParkingSlotUtility.book_parking_slot(parking_slot_id, start_time, end_time)

        # Format booking object into readable dict
        booking_details = BookingUtility.format_booking_details(booking)

        # Send out an email to user
        user = CommonUtility.get_authenticated_user()
        BookingUtility.notify_user_via_email(user, booking_details)

        return booking_details

    @staticmethod
    def cancel_parking_slot_booking(booking_id):

        cancelled = BookingUtility.cancel_booking(booking_id)
        return cancelled

