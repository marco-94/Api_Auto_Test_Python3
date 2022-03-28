"""
新增房源
"""
import time
import unittest
import pysnooper
from utils import login, logout, get_config, get_estate, update_yaml
from erp_property_api import prop, mark


# 打印整个过程的出入参
@pysnooper.snoop(depth=2, max_variable_length=None)
class CreateProperty(unittest.TestCase):
    data = get_config.get_config()

    @classmethod
    def setUpClass(cls):
        """B端用户登录"""
        access_token = login.Login().get_access_token(cls.data["username"], "BPassword")
        update_yaml.UpdateYaml.up_yml("authorization", access_token)
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        """执行结束，退出登录"""
        logout.Logout(cls.data["domain"]).log_out()
        time.sleep(1)

    def test_sale_prop(self):
        """新增二手房住宅"""

        # 先查询小区下房号信息
        get_house = get_estate.Estate().get_estate_info(1, 1)

        # 小区下所有房号被使用了，就直接结束
        while get_house["estate_house_state"]:
            print("该小区下无房号可使用")
            break
        else:
            # 新增多个房源的时候，加上进度条
            for _ in range(1):
                # 新增房源
                response = prop.Prop().sale_prop(get_house)

                # 断言，判断新增是否成功
                self.assertTrue(response["succeed"], msg=response["msg"])

                # 新增失败，直接结束
                if not response["succeed"]:
                    break
                # 新增非正式房源，跳过后面的步骤
                elif response["msg"] == "新增成功，请到我的预录入房源查看":
                    continue
                else:
                    # 房源码信息
                    property_id = response["data"]["propertyId"]

                    # 新增图勘
                    picture_list = mark.Mark(self.data["domain"]).new_mapping(property_id, 1, 1)
                    # 图勘审核
                    mark.Mark(self.data["domain"]).mark_review(property_id, 1, 1, picture_list)

                    # 新增视频
                    mark.Mark(self.data["domain"]).new_video(property_id, 1, 1)
                    # 视频审核
                    mark.Mark(self.data["domain"]).video_review(property_id, 1, 1)

                    # 新增委托书
                    mark.Mark(self.data["domain"]).new_attorney_form(property_id, 1, 1)
                    # 委托书审核
                    mark.Mark(self.data["domain"]).attorney_form_review(property_id, 1, 1)

    def test_rent_prop(self):
        """新增租房住宅"""

        # 先查询小区下房号信息
        get_house = get_estate.Estate().get_estate_info(2, 1)

        # 小区下所有房号被使用了，就直接结束
        while get_house["estate_house_state"]:
            print("该小区下无房号可使用")
            break
        else:
            # 新增房源
            response = prop.Prop().rent_prop(get_house)
            self.assertTrue(response["succeed"], msg=response["msg"])
