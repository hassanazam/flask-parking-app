"""
Idea is to use constants instead of loose strings in whole project
"""


class ConstantsUtility(object):

    STATUS_CODE = "status_code"
    MESSAGE = "message"
    DATA = "data"

    PARKING_AREA = "parking_area"
    PARKING_AREAS = "parking_areas"

    PARKING_SLOTS = "parking_slots"
    PARKING_SLOT = "parking_slot"

    START_TIME = "start_time"
    END_TIME = "end_time"
    PARKING_SLOT_ID = "parking_slot_id"

    BOOKING_DETAILS = "booking_details"
    BOOKED = "booked"
    CANCELLED = "cancelled"

    PARKING_NUMBER_MAX_LENGTH = "PARKING_NUMBER_MAX_LENGTH"

    DATE_TIME_FORMAT = "%d/%m/%Y, %H:%M:%S"

    PARKING_NUMBER = "parking_number"

    ROLE_ID = "role_id"

    ADMIN = "admin"
    CUSTOMER = "customer"
    SUPER_ADMIN = "super_admin"

    ROLE = "role"
    NAME = "name"

    ''' EMAIL CONSTANTS '''
    EMAIL_FROM = 'From'
    EMAIL_TO = 'To'
    EMAIL_MIME_TYPE_PLAIN = 'plain'
    EMAIL_MIME_TYPE_HTML = 'html'

    MIME_SUBJECT = 'Subject'
    KWARGS_ADDRESS = 'address'
    KWARGS_SUBJECT = 'subject'
    KWARGS_TEXT = 'text'
    KWARGS_IS_HTML_TEXT = 'is_html_text'

    BOOKING_EMAIL_TEXT = "Your booking has been made successfully.\n Parking Number : {} \n Start Time : {} " \
                         "\n End Time : {} \n Parking Area : {} \n Parking Slot # {} \n"

    BOOKING_EMAIL_SUBJECT = "Online Parking App"
