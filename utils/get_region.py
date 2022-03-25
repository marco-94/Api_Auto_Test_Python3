"""
获取地域信息
"""

import random
import logging
from utils import get_header, request_method


class Region:
    logging.basicConfig(level=logging.INFO)

    def __init__(self, domain):
        self.domain = domain

    def get_province(self):

        token = get_header.set_token()

        # 获取省份
        get_province_value = {"parentId": 0}
        get_province_response = request_method.RequestMethod.post_method_params(
            self.domain + "/umall.store.api/region/list", token, get_province_value).json()
        province_list = get_province_response["data"]
        province_num = random.randint(0, len(province_list) - 1)
        province_id = province_list[province_num]["regionId"]
        province_name = province_list[province_num]["regionName"]
        return province_id, province_name

    def get_city(self, province_id):
        token = get_header.set_token()

        # 获取城市
        get_city_value = {"parentId": province_id}
        get_city_response = request_method.RequestMethod.post_method_params(
            self.domain + "/umall.store.api/region/list", token, get_city_value).json()
        city_list = get_city_response["data"]
        city_num = random.randint(0, len(city_list) - 1)
        city_id = city_list[city_num]["regionId"]
        city_name = city_list[city_num]["regionName"]
        return city_id, city_name

    def get_regions(self, city_id):
        token = get_header.set_token()

        # 获取区县
        get_region_value = {"parentId": city_id}
        get_region_response = request_method.RequestMethod.post_method_params(
            self.domain + "/umall.store.api/region/list", token, get_region_value).json()
        region_list = get_region_response["data"]
        region_num = random.randint(0, len(region_list) - 1)
        region_id = region_list[region_num]["regionId"]
        region_name = region_list[region_num]["regionName"]
        return region_id, region_name

    def get_street(self, region_id):
        token = get_header.set_token()

        # 获取街道
        get_street_value = {"parentId": region_id}
        get_street_response = request_method.RequestMethod.post_method_params(
            self.domain + "/umall.store.api/region/list", token, get_street_value).json()
        street_list = get_street_response["data"]
        street_num = random.randint(0, len(street_list) - 1)
        street_id = street_list[street_num]["regionId"]
        street_name = street_list[street_num]["regionName"]
        return street_id, street_name
