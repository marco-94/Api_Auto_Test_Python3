"""
封装请求方法
"""
import requests
import urllib3


def method(f):
    def send(self, *args, **kwargs):
        return f(self, *args, **kwargs)
    return send


class RequestMethod:
    urllib3.disable_warnings()

    def __init__(self):
        # 初始化Session
        self.s = requests.Session()
        # 设置忽略https协议
        self.s.verify = False
        # 获取headers，用于后续更新数据
        self.headers = self.s.headers

    def get_method(self, url=None, params=None, **kwargs):
        """封装get方法"""
        try:
            with self.s as req:
                requests.packages.urllib3.disable_warnings()
                res = req.get(url=url, params=params, **kwargs)
            return res
        except Exception as e:
            print("get请求错误: %s" % e)

    @method
    def post_method(self, url=None, data=None, json=None, params=None, **kwargs):
        """封装post方法"""
        try:
            with self.s as req:
                requests.packages.urllib3.disable_warnings()
                res = req.post(url=url, data=data, json=json, params=params, **kwargs)
            return res
        except Exception as e:
            print("post请求错误: %s" % e)

    def delete_method(self, url=None, json=None, params=None, **kwargs):
        """封装delete方法"""
        try:
            with self.s as req:
                requests.packages.urllib3.disable_warnings()
                res = req.delete(url=url, json=json, params=params, **kwargs)
            return res
        except Exception as e:
            print("delete请求错误: %s" % e)

    def put_method(self, url=None, json=None, params=None, **kwargs):
        """封装put方法"""
        try:
            with self.s as req:
                requests.packages.urllib3.disable_warnings()
                res = req.put(url=url, json=json, params=params, **kwargs)
            return res
        except Exception as e:
            print("put请求错误: %s" % e)
