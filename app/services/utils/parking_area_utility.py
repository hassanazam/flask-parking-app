from app import db
from app.models.parking_area import ParkingArea
from app.services.utils.common_utility import CommonUtility


class ParkingAreaUtility(object):

    @staticmethod
    def create_parking_area(name, image):

        parking_area = ParkingArea(name=name, image=image)

        db.session.add(parking_area)
        db.session.commit()

        return parking_area

    @staticmethod
    def get_all_parking_areas():

        parking_areas = ParkingArea.query.all()
        return CommonUtility.convert_to_dict(parking_areas)

    @staticmethod
    def get_parking_area_by_id(area_id):
        area = ParkingArea.query.filter_by(id=area_id).first()
        if area:
            return CommonUtility.convert_to_dict(area)


