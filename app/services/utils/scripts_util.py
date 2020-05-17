from app import db
from app.models.parking_area import ParkingArea
from app.models.parking_slot import ParkingSlot
from app.models.role import Role
from app.services.utils.constants_utility import ConstantsUtility
from app.services.utils.user_utility import UserUtility


class ScriptUtility(object):
    """
    This class holds all the scripts that are required to bootstrap App and DB
    """

    @staticmethod
    def create_super_admin():
        pass


    @staticmethod
    def create_roles():
        """
        For now creating roles in DB manually, Later on they can be created via API from AdminPanel as well.
        :return:
        """

        db.session.add(Role(name=ConstantsUtility.ADMIN))
        db.session.add(Role(name=ConstantsUtility.CUSTOMER))

        db.session.commit()

    @staticmethod
    def bootstrap_test_data():

        p_area = ParkingArea(name="Lucky One | Ground Floor")

        db.session.add(p_area)
        db.session.commit()

        db.session.add(ParkingSlot(parking_area_id=p_area.id))
        db.session.add(ParkingSlot(parking_area_id=p_area.id))

        db.session.commit()

    @staticmethod
    def create_admin(email, password):

        admin = UserUtility.create_admin(email, password)
        print(" Admin email address : {}".format(str(email)))
        print(" Admin password : {}".format(str(password)))
        print(" Admin created!")
