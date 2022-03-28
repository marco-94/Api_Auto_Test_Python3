"""
房源配套设施
"""
import random
import math


class PropertyDeviceItems:
    @staticmethod
    def property_device_items(property_type):
        """
        配套设施字典：1.住宅类(property_device_items)；2.商铺类(shop_device_items)；3.写字楼类(offices_device_items)\n
        :return: 配套设施编码列表
        """
        return_json = {
            "property_device_items_list": []
        }

        # 随机勾选0~10个标签
        for _ in range(random.randint(0, 10)):
            if property_type is None:
                break
            elif property_type == 1:
                return_json["property_device_items_list"].append(int(math.pow(2, random.randint(0, 17))))
            elif property_type == 2:
                return_json["property_device_items_list"].append(int(math.pow(2, random.randint(0, 15))))
            elif property_type == 3:
                return_json["property_device_items_list"].append(int(math.pow(2, random.randint(0, 11))))

        # 去掉重复标签
        return_json["property_device_items_list"] = list(set(return_json["property_device_items_list"]))

        return return_json
