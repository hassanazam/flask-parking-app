import json


def login_user(app_context, email, password):

    with app_context as test_app:

        url = "/auth"

        payload = {
            "username": email,
            "password": password
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = test_app.post(url, headers=headers, json=payload)

        print(response.data)
        resp_json = json.loads(response.data)
        return resp_json


def register_user(app_context, email, password):

    with app_context as test_app:

        req_data = {
            "email": email,
            "password": password
        }
        resp = test_app.post("/user/register", json=req_data)
        print(resp.data)
        resp_json = json.loads(resp.data)


def setup_test_data():

    from app.services.utils.scripts_util import ScriptUtility

    ScriptUtility.create_roles()
    ScriptUtility.create_admin("testadmin@mailinator.com", "testadmin")

    ScriptUtility.bootstrap_test_data()


def book_parking_slot(app_context, start_time, end_time, slot_id, jwt_token):

    with app_context as test_app:

        req_data = {
            "start_time": int(start_time/1000),
            "end_time": int(end_time/1000),
            "parking_slot_id": slot_id,
        }

        headers = {
            "Authorization": "JWT {}".format(jwt_token)
        }

        resp = test_app.post("/parking-slot/book", json=req_data, headers=headers)
        print(resp.data)
        resp_json = json.loads(resp.data)
        return resp_json

