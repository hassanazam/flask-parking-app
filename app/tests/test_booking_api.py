import json
import os
import unittest
from unittest.mock import patch


class TestBookingAPI(unittest.TestCase):

    # Mock env variable APP_CONFIG_PATH
    # It contains the path of required external config file
    def setUp(self):

        with patch.dict('os.environ', {"APP_CONFIG_PATH": "D:/HassanWorkSpace/flask-parking-app/parking_app_test_config.py"}):

            from app import app, db
            self.app = app
            self.db = db

            # Initialize test environment database
            db.create_all()

            # Setup test data
            from app.tests.test_register_api import setup_test_data
            setup_test_data()

            self.test_app_client = app.test_client()

        from app.tests.test_base import login_user

        from app.tests.test_base import register_user
        register_user(self.test_app_client, "newuser@mailinator.com", "12345")
        token_resp = login_user(self.test_app_client, "newuser@mailinator.com", "12345")
        self.jwt_token = token_resp["access_token"]

    def test_booking_api_success(self):

        # Prepare test data for API
        from app.services.utils.common_utility import CommonUtility
        request_data = {
            "start_time": int(CommonUtility.get_time()/1000),   # Convert to secs
            "end_time": int(CommonUtility.get_time(offset=1)/1000),
            "parking_slot_id": 1
        }

        headers = {
            "Authorization": "JWT {}".format(self.jwt_token)
        }

        resp = None
        with self.test_app_client as c:
            resp = c.post("/parking-slot/book", json=request_data, headers=headers)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("Success", resp_json.get("message"))
        self.assertEqual(0, resp_json["status_code"])

    def test_booking_api_with_start_time_less_than_current_time(self):

        # Prepare test data for API
        from app.services.utils.common_utility import CommonUtility
        request_data = {
            "start_time": int(CommonUtility.get_time(offset=-1)/1000),
            "end_time": int(CommonUtility.get_time()/1000),
            "parking_slot_id": 1
        }

        headers = {
            "Authorization": "JWT {}".format(self.jwt_token)
        }

        resp = None
        with self.test_app_client as c:
            resp = c.post("/parking-slot/book", json=request_data, headers=headers)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("Parking start time cannot be less than current time!", resp_json.get("message"))
        self.assertEqual(105, resp_json["status_code"])


    def test_booking_api_with_end_time_less_than_current_time(self):

        # Prepare test data for API
        from app.services.utils.common_utility import CommonUtility
        request_data = {
            "start_time": int(CommonUtility.get_time()/1000),
            "end_time": int(CommonUtility.get_time(offset=-1)/1000),
            "parking_slot_id": 1
        }

        headers = {
            "Authorization": "JWT {}".format(self.jwt_token)
        }

        resp = None
        with self.test_app_client as c:
            resp = c.post("/parking-slot/book", json=request_data, headers=headers)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("Parking end time cannot be less than current time!", resp_json.get("message"))
        self.assertEqual(105, resp_json["status_code"])

    def test_booking_api_with_already_booked_slot(self):

        # Prepare test data for API
        from app.services.utils.common_utility import CommonUtility
        request_data = {
            "start_time": int(CommonUtility.get_time()/1000),   # Convert to secs
            "end_time": int(CommonUtility.get_time(offset=1)/1000),
            "parking_slot_id": 1
        }

        headers = {
            "Authorization": "JWT {}".format(self.jwt_token)
        }

        resp = None
        with self.test_app_client as c:
            resp_dup = c.post("/parking-slot/book", json=request_data, headers=headers)
            # Another request trying to book the same slot for the same date time
            resp = c.post("/parking-slot/book", json=request_data, headers=headers)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("This slot is already booked for the given time.", resp_json.get("message"))
        self.assertEqual(103, resp_json["status_code"])


    def tearDown(self):

        # Flush test db
        self.db.session.remove()
        self.db.drop_all()
