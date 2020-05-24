import json
import os
import unittest
from unittest.mock import patch


class TestAdminAPIs(unittest.TestCase):

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

        from app.tests.test_base import login_user
        resp = login_user(self.test_app_client, "testadmin@mailinator.com", "testadmin")
        self.admin_jwt_token = resp["access_token"]

        # Make booking, for which Cancel API test cases will be executed
        from app.tests.test_base import book_parking_slot
        from app.services.utils.common_utility import CommonUtility
        from app.tests.test_base import login_user
        from app.tests.test_base import register_user

        # Setup scenario for Cancelling API

        register_user(self.test_app_client, "newuser@mailinator.com", "12345")
        token_resp = login_user(self.test_app_client, "newuser@mailinator.com", "12345")
        self.user_jwt_token = token_resp["access_token"]

        self.booking1 = book_parking_slot(self.test_app_client, CommonUtility.get_time(), CommonUtility.get_time(1), 1,
                                     self.user_jwt_token)

        self.booking2 = book_parking_slot(self.test_app_client, CommonUtility.get_time(2), CommonUtility.get_time(3), 1,
                                     self.user_jwt_token)

        self.booking3 = book_parking_slot(self.test_app_client, CommonUtility.get_time(4), CommonUtility.get_time(5), 1,
                                     self.user_jwt_token)

    def test_view_booking_details(self):

        # Made some bookings
        from app.tests.test_base import book_parking_slot
        from app.services.utils.common_utility import CommonUtility

        headers = {"Authorization": "JWT {}".format(self.admin_jwt_token)}

        with self.test_app_client as t:
            resp = t.get("/admin/bookings", headers=headers)

        json_response = json.loads(resp.data)
        print(json_response)

    def test_cancel_api_success_by_admin(self):

        # Prepare test data for API
        request_data = {
            "booking_id": self.booking1["data"]["booking_details"]["id"]
        }

        headers = {"Authorization": "JWT {}".format(self.admin_jwt_token)}

        resp = None
        with self.test_app_client as c:
            resp = c.post("/parking-slot/cancel-booking", json=request_data, headers=headers)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("Your booking has been cancelled.", resp_json["message"])
        self.assertEqual(0, resp_json["status_code"])

        with self.test_app_client as t:
            details_resp = t.get("/admin/bookings", headers=headers)

        print(details_resp.data)

    def test_view_user_data_api(self):

        headers = {
            "Authorization": "JWT {}".format(self.admin_jwt_token)
        }

        with self.test_app_client as t:
            resp = t.get("/admin/users", headers=headers)

        print(json.loads(resp.data))

    def test_view_user_data_api_with_unauthorized(self):

        headers = {
            "Authorization": "JWT {}".format(self.user_jwt_token)
        }

        with self.test_app_client as t:
            resp = t.get("/admin/users", headers=headers)

        print(resp.data)

        # Should return 401, because we are trying to access ADMIN api with User's token
        self.assertEqual(401, resp.status_code)

    def tearDown(self):

        # Flush test db
        self.db.session.remove()
        self.db.drop_all()
