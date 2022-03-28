"""
新增住宅
"""
import random
import urllib3
import json
from utils import get_header, get_config, request_method, get_phone, get_name, data_handle


class Prop:
    data = get_config.get_config()
    urllib3.disable_warnings()

    # 房源标题信息
    rent_subject = "租房住宅户型方正 绿色家园 居住舒适"
    sale_subject = "二手房住宅单元楼下车位方正出入方便"

    ownerPhone = get_phone.Phone.create_phone()

    def sale_prop(self, get_house_json):
        """
        新增二手房住宅
        :param: get_house_json：房号信息json
        :return:
        """
        token = get_header.set_token()

        # 设置建筑面积和使用面积
        structure_area = random.randint(120, 150)
        useful_area = structure_area - 5

        # 设置住宅价格：售价、底价（90%）、首付（30%）、欠款（10%）、可贷（售价减去首付）、月供（贷款10年）
        sale_price = random.randint(100, 150)
        floor_price = sale_price * 0.9
        first_pay_amount = sale_price * 0.3
        deoto_amount = sale_price * 0.1
        loan_amount = sale_price - first_pay_amount
        monthly_pay_amount = loan_amount * 10000 / 120

        # 新增房源
        add_sale_value = {
            "salePrice": sale_price,
            "floorPrice": floor_price,
            "firstPayAmount": first_pay_amount,
            "deotoAmount": deoto_amount,
            "loanAmount": loan_amount,
            "monthlyPayAmount": monthly_pay_amount,
            "structureArea": structure_area,
            "usefulArea": useful_area,
            "subject": self.sale_subject + str(random.randint(0, 99999)).zfill(5),
            "taxType": random.randint(1, 5)
        }
        print("新增二手房住宅：" + str(json.dumps(add_sale_value, ensure_ascii=False)))
        add_sale_response = request_method.RequestMethod().post_method(
            url=self.data["domain"] + "",
            headers=token,
            json=add_sale_value).json()
        print(data_handle.DataHandle.response_json_dumps(add_sale_response))
        return add_sale_response

    def rent_prop(self, get_house_json):
        """
        新增租房住宅
        :param get_house_json：房号信息json
        :return:
        """
        token = get_header.set_token()

        # 新增房源
        add_rent_prop_value = {
            "selfRulePropertyFlag": False,
            "rentalType": random.randint(1, 2),
            "ownerPhone": self.ownerPhone,
            "ownerOtherPhone": get_phone.Phone.create_phone(),
            "rentPrice": random.randint(3400, 3600),
            "subject": self.rent_subject + str(random.randint(0, 99999)).zfill(5),
            "buildingsName": get_house_json["estate_buildings_name"],
            "adminAddress": self.data["admin_address"],
            "ownerName": get_name.TestTest.create_name()
        }
        print("新增租房住宅：" + str(json.dumps(add_rent_prop_value, ensure_ascii=False)))
        add_rent_prop_response = request_method.RequestMethod().post_method(
            url=self.data["domain"] + "",
            headers=token,
            json=add_rent_prop_value).json()
        print(data_handle.DataHandle.response_json_dumps(add_rent_prop_response))
        return add_rent_prop_response
