# coding=utf-8
"""
获取各种格式时间
"""
import time
import datetime


class GetTime:
    @staticmethod
    def get_the_day_before_time():
        """
        获取当天和前一天时间的北京时间和时间戳(零点)
        :return:
        """
        t = datetime.datetime.now()
        today = t.strftime('%Y-%m-%d 00:00:00')
        today_time = str((time.mktime(time.strptime(today, '%Y-%m-%d %H:%M:%S'))) * 1000).split(".")[0]

        before_day = (t + datetime.timedelta(days=-1)).strftime("%Y-%m-%d 00:00:00")
        before_day_time = str((time.mktime(time.strptime(before_day, '%Y-%m-%d %H:%M:%S'))) * 1000).split(".")[0]

        return before_day_time, today_time, today, before_day

    @staticmethod
    def get_current_time():
        """
        获取当前时间的时间戳和北京时间
        """

        current_time = round(time.time() * 1000)
        current_time_beijing = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        return current_time, current_time_beijing
