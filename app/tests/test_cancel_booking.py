import json
import os
import unittest
from unittest.mock import patch


class TestCancelBookingAPI(unittest.TestCase):

    def setUp(self):

        # Set up env variable APP_CONFIG_PATH
        # It contains the path of required external config file

        with patch.dict('os.environ', {"APP_CONFIG_PATH": "D:/HassanWorkSpace/flask-parking-app/parking_app_test_config.py"}):
            from app import app, db
            self.app = app
            self.db = db

            # Initialize test environment database
            db.create_all()

            # Setup test data
            from app.tests.test_base import setup_test_data
            setup_test_data()

            self.test_app_client = app.test_client()

        # Make booking, for which Cancel API test cases will be executed
        from app.tests.test_base import book_parking_slot
        from app.services.utils.common_utility import CommonUtility
        from app.tests.test_base import login_user
        from app.tests.test_base import register_user

        # Setup scenario for Cancelling API

        register_user(self.test_app_client, "newuser@mailinator.com", "12345")
        token_resp = login_user(self.test_app_client, "newuser@mailinator.com", "12345")
        self.jwt_token = token_resp["access_token"]
        self.booking = book_parking_slot(self.test_app_client, CommonUtility.get_time(), CommonUtility.get_time(1), 1,
                                    self.jwt_token)
        print(self.booking)

    def test_cancel_api_success(self):

        # Prepare test data for API
        request_data = {
            "booking_id": self.booking["data"]["booking_details"]["id"]
        }

        headers = {"Authorization": "JWT {}".format(self.jwt_token)}

        resp = None
        with self.test_app_client as c:
            resp = c.post("/parking-slot/cancel-booking", json=request_data, headers=headers)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("Your booking has been cancelled.", resp_json["message"])
        self.assertEqual(0, resp_json["status_code"])

    def test_cancel_api_with_wrong_booking_id(self):

        # Prepare test data for API
        request_data = {
            "booking_id": 1111111
        }

        headers = {"Authorization": "JWT {}".format(self.jwt_token)}

        resp = None
        with self.test_app_client as c:
            resp = c.post("/parking-slot/cancel-booking", json=request_data, headers=headers)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("Invalid booking id", resp_json["message"])
        self.assertEqual(104, resp_json["status_code"])

    def test_cancel_api_with_already_cancelled_booking(self):

        # Prepare test data for API
        request_data = {
            "booking_id": self.booking["data"]["booking_details"]["id"]
        }

        headers = {"Authorization": "JWT {}".format(self.jwt_token)}

        resp = None
        with self.test_app_client as c:
            _resp = c.post("/parking-slot/cancel-booking", json=request_data, headers=headers)
            resp = c.post("/parking-slot/cancel-booking", json=request_data, headers=headers)
            print(resp.data)

        resp_json = json.loads(resp.data)


        self.assertEqual("This booking has already cancelled.", resp_json["message"])
        self.assertEqual(106, resp_json["status_code"])

    def test_cancel_api_with_success_and_then_rebooking(self):

        from app.tests.test_base import book_parking_slot
        from app.services.utils.common_utility import CommonUtility
        start_time = CommonUtility.get_time()
        end_time = CommonUtility.get_time(1)
        slot_id = 2
        local_booking = book_parking_slot(self.test_app_client, start_time, end_time, slot_id, self.jwt_token)

        # Prepare test data for API
        request_data = {
            "booking_id": local_booking["data"]["booking_details"]["id"]
        }

        headers = {"Authorization": "JWT {}".format(self.jwt_token)}

        resp = None
        with self.test_app_client as c:
            resp = c.post("/parking-slot/cancel-booking", json=request_data, headers=headers)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("Your booking has been cancelled.", resp_json["message"])
        self.assertEqual(0, resp_json["status_code"])

        # Rebook the same slot again to verify cancellation
        local_booking = book_parking_slot(self.test_app_client, start_time, end_time, slot_id, self.jwt_token)
        print("Rebooking Response")
        print(local_booking)

    def tearDown(self):

        # Flush test db
        self.db.session.remove()
        self.db.drop_all()
