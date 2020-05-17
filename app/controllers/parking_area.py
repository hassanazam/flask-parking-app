from app.services.utils.common_utility import CommonUtility
from app.services.utils.parking_area_utility import ParkingAreaUtility
from app.services.utils.parking_slot_utility import ParkingSlotUtility


class ParkingAreaController(object):

    @staticmethod
    def create_parking_area(name, image):

        parking_area = ParkingAreaUtility.create_parking_area(name, image)

        return CommonUtility.convert_to_dict(parking_area)


    @staticmethod
    def list_parking_areas():

        parking_areas = ParkingAreaUtility.get_all_parking_areas()

        return parking_areas

    @staticmethod
    def list_slots_of_parking_area(area_id):

        parking_slots = ParkingSlotUtility.get_all_slots_by_area_id(area_id)

        return parking_slots
