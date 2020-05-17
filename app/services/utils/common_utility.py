from flask import request


class CommonUtility(object):

    @staticmethod
    def get_request_data():
        return request.get_json(force=True, silent=True) or {}
