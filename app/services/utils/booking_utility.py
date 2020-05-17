from sqlalchemy import and_, or_

from app import db, app
from app.models.booking import Booking
from app.models.parking_area import ParkingArea
from app.models.parking_slot import ParkingSlot
from app.services.utils.common_utility import CommonUtility
from app.services.utils.constants_utility import ConstantsUtility
from app.services.utils.exception_utility import APIException
from app.services.utils.response_utility import ResponseInfo


class BookingUtility(object):

    @staticmethod
    def get_booking_by_slot_id_and_time(parking_slot_id, start_time, end_time):
        """
        Find any booking that lies in the given time range
        :param parking_slot_id:
        :param start_time:
        :param end_time:
        :return:
        """

        booking = db.session.query(Booking).filter(and_(
            Booking.parking_slot_id == parking_slot_id,
            Booking.status == ConstantsUtility.BOOKED,
            or_(and_(start_time >= Booking.start_time, start_time <= Booking.end_time),
            and_(end_time >= Booking.start_time, end_time <= Booking.end_time)))).first()

        return booking

    @staticmethod
    def create_booking(slot_id, start_time, end_time):
        """
        Create booking entry for given parking slot.
        :param slot_id:
        :param start_time:
        :param end_time:
        :return:
        """

        user = CommonUtility.get_authenticated_user()

        booking = Booking(parking_slot_id=slot_id, start_time=start_time, end_time=end_time,
                          status=ConstantsUtility.BOOKED, user_id=user.id)

        db.session.add(booking)
        db.session.commit()

        return booking

    @staticmethod
    def format_booking_details(booking):
        """
        Transform booking object into readable form
        :param booking:
        :return:
        """

        parking_slot = ParkingSlot.query.filter_by(id=booking.parking_slot_id).first()
        parking_area = ParkingArea.query.filter_by(id=parking_slot.parking_area_id).first()

        parking_number = BookingUtility.get_parking_number(booking)

        start_time = CommonUtility.get_date_from_epoch(booking.start_time, ConstantsUtility.DATE_TIME_FORMAT)
        end_time = CommonUtility.get_date_from_epoch(booking.end_time, ConstantsUtility.DATE_TIME_FORMAT)

        return {
            "id": booking.id,
            ConstantsUtility.PARKING_AREA: parking_area.name,
            ConstantsUtility.PARKING_SLOT: parking_slot.id,
            ConstantsUtility.PARKING_NUMBER: parking_number,
            ConstantsUtility.START_TIME: start_time,
            ConstantsUtility.END_TIME: end_time
        }

    @staticmethod
    def get_parking_number(booking):
        """
        It generates a unique parking number based on the ID of booking entry
        Scheme:
        A configurable length of parking_number (6)
        6 * "0" = 000000
        000000 + 22(id of booking) = 000022 -> parking number
        :param booking:
        :return:
        """

        max_length = app.config[ConstantsUtility.PARKING_NUMBER_MAX_LENGTH]

        mask = max_length * "0"
        parking_number = str(mask[len(str(booking.id)):]) + str(booking.id)

        return str(parking_number)

    @staticmethod
    def cancel_booking(booking_id):

        booking = Booking.query.filter_by(id=booking_id).first()
        if not booking:
            raise APIException(status_code=ResponseInfo.CODE_INVALID_BOOKING_ID,
                               message=ResponseInfo.MESSAGE_INVALID_BOOKING_ID)

        # Update status as cancelled
        booking.status = ConstantsUtility.CANCELLED

        db.session.commit()
        return True
