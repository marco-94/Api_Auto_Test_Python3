"""
退出登录
"""
from utils import request_method, get_header, update_yaml


class Logout:
    def __init__(self, domain):
        self.domain = domain

    def log_out(self):

        token = get_header.set_token()

        log_out_response = request_method.RequestMethod.get_method(self.domain + "", token).json()
        update_yaml.UpdateYaml.up_yml("authorization", None)
        update_yaml.UpdateYaml.up_yml("authorization-c", None)
        print("退出登录：", log_out_response)