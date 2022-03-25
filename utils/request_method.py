"""
封装请求方法
"""
import requests


class RequestMethod:

    @staticmethod
    def get_method(url, headers=None, params1=None):
        """封装get方法"""
        try:
            res = requests.get(url=url, headers=headers, params=params1)
            return res
        except Exception as e:
            print("get请求错误: %s" % e)

    @staticmethod
    def post_method_params(url, headers, params1=None):
        """封装post方法"""
        try:
            res = requests.post(url=url, headers=headers, params=params1)
            return res
        except Exception as e:
            print("post请求错误: %s" % e)

    @staticmethod
    def post_method(url, headers, json1=None):
        """封装post方法"""
        try:
            res = requests.post(url=url, headers=headers, json=json1)
            return res
        except Exception as e:
            print("post请求错误: %s" % e)

    @staticmethod
    def delete_method(url, headers, json1=None):
        """封装delete方法"""
        try:
            res = requests.delete(url=url, headers=headers, json=json1)
            return res
        except Exception as e:
            print("delete请求错误: %s" % e)

    @staticmethod
    def put_method(url, headers, json1=None):
        """封装put方法"""
        try:
            res = requests.put(url=url, headers=headers, json=json1)
            return res
        except Exception as e:
            print("put请求错误: %s" % e)
