"""
Controller for displaying Booking Details to ADMIN
"""
from app.services.utils.booking_utility import BookingUtility


class BookingDetailsController(object):

    @staticmethod
    def get_booking_details():

        bookings = BookingUtility.read_all_booking_details()

        formatted_details = []

        for booking in bookings:
            fb = BookingUtility.format_booking_details(booking)
            formatted_details.append(fb)

        return formatted_details
