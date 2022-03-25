"""
获取请求头信息
"""
from utils import get_config


def set_token():
    data = get_config.get_config()
    headers = {"Content-Type": "application/json;charset=UTF-8",
               "x-brand-id": data["X-Brand-Id"],
               "x-organ-id": data["X-Organ-Id"],
               "x-city-code": data["X-City-Code"],
               "authorization": data["authorization"]}
    return headers

def set_token_c():
    data = get_config.get_config()
    headers = {"Content-Type": "application/json;charset=UTF-8",
               "authorization": data["authorization-c"]}
    return headers