# coding: utf-8

from datetime import datetime, timedelta


class DateTools(object):

    # date 转换成string
    @staticmethod
    def date_format(dt):
        if not isinstance(dt, datetime):
            return None
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # 字符串转换为date
    @staticmethod
    def str_format(s_time):
        try:
            return datetime.strptime(s_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

    # 变动固定时间
    # dt 为时间datetime类, add 默认为减少
    @staticmethod
    def update_time(dt, add=False, minutes=0, hours=0, days=0, mouths=0, years=0):
        if not isinstance(dt, datetime):
            return None
        update_date_minutes = minutes + 60 * hours + 60 * 24 * days + 60 * 24 * 30 * mouths + 60 * 24 * 30 * 365 * years
        if add:
            return dt + timedelta(minutes=update_date_minutes)
        else:
            return dt - timedelta(minutes=update_date_minutes)
