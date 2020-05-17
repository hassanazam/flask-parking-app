from functools import wraps

from flask import jsonify

from app.services.utils.exception_utility import APIException
from app.services.utils.response_utility import Response


def api_response_handler(view_func):
    """
    This decorator handles custom raised API exceptions while processing of request.
    It catches the exception gracefully and return appropriate response to the client
    with proper status_code and message.
    """

    @wraps(view_func)
    def response_decorator(*args, **kwargs):

        try:
            response = view_func(*args, **kwargs)
        except APIException as api_exception:
            response = Response(api_exception.status_code, api_exception.message, api_exception.data)
            return jsonify(response.to_dict())

        return response

    return response_decorator

