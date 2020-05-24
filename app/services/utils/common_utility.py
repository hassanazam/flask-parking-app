import datetime
import time

from flask import request, g


class CommonUtility(object):

    @staticmethod
    def get_request_data():
        return request.get_json(force=True, silent=True) or {}

    @staticmethod
    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        return d

    @staticmethod
    def convert_to_dict(alchemy_objs):
        if isinstance(alchemy_objs, list):
            result = []
            for obj in alchemy_objs:
                result.append(CommonUtility.row2dict(obj))
            return result
        else:
            return CommonUtility.row2dict(alchemy_objs)

    @staticmethod
    def get_date_from_epoch(time_in_secs, date_format):
        if time_in_secs:
            return datetime.datetime.fromtimestamp(time_in_secs).strftime(date_format)

    @staticmethod
    def get_authenticated_user():

        return getattr(g, "authenticated_user")

    @staticmethod
    def get_time(offset=0):
        """
        return serialized datetime current + offset in hours
        It returns time in epoch format (msecs)
        """
        return time.mktime(
            (datetime.datetime.now() + datetime.timedelta(hours=offset)).timetuple()) * 1000
