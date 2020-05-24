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

