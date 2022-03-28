"""
查询小区信息
"""
from utils import get_header, request_method, get_config, get_time


class Estate:

    data = get_config.get_config()

    def get_estate_info(self, property_type, query_type, buildings_id=None, buildings_name=None, unit_id=None,
                        unit_no=None, page_no=None, house_no=None, house_id=None):
        """
        获取二手房小区楼栋单元房号等信息\n
        :param property_type: 租售类型：1.二手房，2.租房；
        :param query_type: 房源类型：1.住宅，2.别墅，3.商住两用，4.车位，5.商铺，6.写字楼,7.厂房,8.土地；
        :param buildings_id: 楼栋ID
        :param buildings_name: 楼栋名称
        :param unit_id: 单元ID
        :param unit_no: 单元名称
        :param page_no: 分页
        :param house_no: 房号名称
        :param house_id: 房号ID
        :return: json格式，包含字段：楼栋ID、楼栋名称、单元ID、单元名称、房号ID、房号名称、当前楼层、总楼层、
        小区下是否全部房号被使用(false未使，true未全部使用)
        """
        if property_type == 1:
            property_type = "sale"
        elif property_type == 2:
            property_type = "rent"
        else:
            print("租售类型不正确")

        # 翻页默认第一页
        if page_no is None:
            page_no = 1

        # 最终返回的小区楼栋单元房号信息json
        return_json = {
            "estate_name": self.data["estate_name"]
        }

        token = get_header.set_token()

        # 获取当前条件的小区/楼栋/单元下的房号列表
        get_house_value = {
            "houseId": house_id,
            "cityCode": self.data["X-City-Code"],
            "estateCode": self.data["estate_code"],
            "buildingsId": buildings_id,
            "buildingsName": buildings_name,
            "unitId": unit_id,
            "unitNo": unit_no,
            "houseNo": house_no,
            "pageNo": page_no,
            "pageSize": 2000
        }

        get_house_response = request_method.RequestMethod.get_method(
            self.data["domain"] + "", token, get_house_value).json()
        house_no_list = get_house_response["data"]["list"]

        # 定义车位/写字楼/商铺/厂房类房源的房号
        prop_no = get_time.GetTime.get_current_time()[0]

        # 轮询房号列表的每一个房号，并检查是否被使用
        check_estate_house_no_value = {}
        for i in range(len(house_no_list)):
            # 如果是住宅/别墅/商住两用，就用房号去判断
            if query_type == 1 or query_type == 2 or query_type == 3:
                check_estate_house_no_value = {
                    "category": query_type,
                    "estateId": self.data["estate_code"],
                    "propNo": get_house_response["data"]["list"][i]["houseNo"],
                    "propertyId": get_house_response["data"]["list"][i]["houseId"],
                    "building": get_house_response["data"]["list"][i]["buildingsName"],
                    "unit": get_house_response["data"]["list"][i]["unitNo"]
                }
            # 如果是车位/写字楼/商铺/厂房，就用当前时间的时间戳去判断(因为楼栋/单元/房号信息可自定义)
            elif query_type == 4 or query_type == 5 or query_type == 6 or query_type == 7:
                check_estate_house_no_value = {
                    "category": query_type,
                    "estateId": self.data["estate_code"],
                    "propNo": get_time.GetTime.get_current_time()[0],
                    "building": get_house_response["data"]["list"][i]["buildingsName"],
                    "unit": get_house_response["data"]["list"][i]["unitNo"]
                }
            # 根据传入的类型，查询租房或者二手房
            check_estate_house_no_response = request_method.RequestMethod.post_method(
                self.data["domain"] + "" + property_type, token,
                check_estate_house_no_value).json()
            estate_house_no_state = check_estate_house_no_response["data"]["isExist"]
            return_json["estate_house_state"] = estate_house_no_state

            # 如果被使用，跳过，继续查找；如果没被使用，结束循环，返回房号信息，更新前面定义好的需要return的字段
            if estate_house_no_state:
                continue
            elif not estate_house_no_state:
                # 楼栋信息
                return_json["estate_buildings_id"] = get_house_response["data"]["list"][i]["buildingsId"]
                return_json["estate_buildings_name"] = get_house_response["data"]["list"][i]["buildingsName"]
                # 单元信息
                return_json["estate_unit_id"] = get_house_response["data"]["list"][i]["unitId"]
                return_json["estate_unit_no"] = get_house_response["data"]["list"][i]["unitNo"]
                # 房号信息：如果是住宅/别墅/商住两用，房号就是楼盘字典的房号
                return_json["estate_house_no"] = get_house_response["data"]["list"][i]["houseNo"]
                if query_type == 1 or query_type == 2 or query_type == 3:
                    return_json["estate_house_id"] = get_house_response["data"]["list"][i]["houseId"]
                # 如果是车位/写字楼/商铺/厂房，房号就是当前时间的时间戳(因为楼栋/单元/房号信息可自定义)
                elif query_type == 4 or query_type == 5 or query_type == 6 or query_type == 7:
                    return_json["estate_house_id"] = prop_no
                # 楼层信息
                return_json["actual_floor_no"] = get_house_response["data"]["list"][i]["actualFloorNo"]
                return_json["actual_total_floor_no"] = get_house_response["data"]["list"][i]["actualTotalfloorNo"]
                break

        return return_json
