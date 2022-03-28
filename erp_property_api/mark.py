"""
新增标记
"""
import time
import string
import random
import requests
from faker import Faker
from utils import get_header, file_upload, get_config, request_method, get_name, get_time
from erp_property_api import property_picture_set


class Mark:
    data = get_config.get_config()

    fake = Faker(locale='zh_CN')

    def __init__(self, domain):
        self.domain = domain

    def new_mapping(self, property_id, trans_type, property_category):
        """
        新增图勘\n
        :param property_id: 房源码
        :param trans_type: 租售类型：1.二手房，2.租房；
        :param property_category: 房源类型：1.住宅，2.别墅，3.商住两用，4.车位，5.商铺，6.写字楼,7.厂房,8.土地；
        :return: json格式，包含字段：环境图、户型图、室内图
        """

        token = get_header.set_token()

        # 设置房源图片
        return_json = {
            "house_type": property_picture_set.PropertyPicture(self.data["domain"]).property_picture(2, 4)[
                "property_picture_list"],
            "indoor": property_picture_set.PropertyPicture(self.data["domain"]).property_picture(3, 4)[
                "property_picture_list"],
            "environment": property_picture_set.PropertyPicture(self.data["domain"]).property_picture(4, 4)[
                "property_picture_list"]
        }

        save_mark_prospect_value = {
            "estateId": self.data["estate_code"],
            "propertyCategory": property_category,
            "propertyId": property_id,
            "transType": trans_type,
            "markTm": get_time.GetTime.get_current_time()[0],
            "remarks": "测试图勘",
            "filesEnvironment": return_json["environment"],
            "filesHouseType": return_json["house_type"],
            "filesIndoor": return_json["indoor"],
            "cityCode": self.data["X-City-Code"]
        }

        save_mark_prospect_response = request_method.RequestMethod.post_method(
            self.domain + "", token, save_mark_prospect_value).json()

        print("新增图勘：", str(save_mark_prospect_response))
        return return_json

    def mark_review(self, property_id, trans_type, property_category, picture_list):
        """
        图片标记审核\n
        :param property_id: 房源码
        :param trans_type: 租售类型，1.二手房；2.租房；
        :param property_category: 房源类型：1.住宅，2.别墅，3.商住两用，4.车位，5.商铺，6.写字楼,7.厂房,8.土地；
        :param picture_list: 图勘地址字典
        :return:
        """
        token = get_header.set_token()

        # 查询标记列表
        mark_list_value = {
            "pageNo": 1,
            "pageSize": 1,
            "markCategory": 1,
            "propertyId": property_id,
            "transType": trans_type
        }

        mark_list_response = None
        for _ in range(3):
            mark_list_response = request_method.RequestMethod.post_method(
                self.domain + "", token, mark_list_value).json()

            if not mark_list_response["data"]["list"]:
                time.sleep(3)
                continue
            else:
                break

        mark_status = mark_list_response["data"]["list"][0]["status"]
        pk_id = mark_list_response["data"]["list"][0]["propertyMarkId"]

        print("图勘状态：", str(mark_status))

        if mark_status == 0:
            value_mark_review = {
                "cityCode": self.data["X-City-Code"],
                "pkId": pk_id,
                "propertyId": property_id,
                "status": "1",
                "operateRemarks": "这个是图勘审核备注",
                "propertyCategory": property_category,
                "filesEnvironment": picture_list["environment"],
                "filesHouseType": picture_list["house_type"],
                "filesIndoor": picture_list["indoor"]
            }
            mark_review_response = request_method.RequestMethod.post_method(
                self.domain + "", token, value_mark_review).json()
            print("图勘审核：", str(mark_review_response))

    def new_video(self, property_id, trans_type, property_category):
        """
        新增房源视频
        :param property_id: 房源码
        :param trans_type: 租售类型，1.二手房；2.租房；
        :param property_category: 房源类型：1.住宅，2.别墅，3.商住两用，4.车位，5.商铺，6.写字楼,7.厂房,8.土地；
        :return:
        """

        token = get_header.set_token()

        print("开始上传视频")
        url = file_upload.Upload(self.data["domain"]).upload_video(1)
        print("上传视频完成")

        value_video = {
            "estateId": self.data["estate_code"],
            "propertyCategory": property_category,
            "propertyId": property_id,
            "transType": trans_type,
            "markTm": get_time.GetTime.get_current_time()[0],
            "remarks": "测试视频",
            "agentId": "",
            "propertyMarkId": "",
            "cityCode": self.data["X-City-Code"],
            "applyPrice": "",
            "applyUnit": 1,
            "files": [
                {
                    "bucket": "yjyz-beta-sz",
                    "name": "test-video.mp4",
                    "size": 3957823,
                    "type": "video",
                    "url": url[1],
                    "fullUrl": url[0]
                }
            ]
        }

        response_video = requests.post(url="", json=value_video, headers=token).json()

        print("新增视频：", str(response_video))
        time.sleep(3)

    def video_review(self, property_id, trans_type, property_category):
        """
        视频标记审核
        :param property_id: 房源码
        :param trans_type: 租售类型，1.二手房；2.租房；
        :param property_category: 房源类型：1.住宅，2.别墅，3.商住两用，4.车位，5.商铺，6.写字楼,7.厂房,8.土地；
        :return:
        """
        token = get_header.set_token()

        # 查询标记列表
        value_video_list = {
            "pageNo": 1,
            "pageSize": 1,
            "markCategory": 3,
            "estateName": self.data["estate_name"],
            "propertyId": property_id,
            "transType": trans_type
        }

        response_video_list = request_method.RequestMethod.post_method(
            self.domain + "", token, value_video_list).json()

        video_status = response_video_list["data"]["list"][0]["status"]
        video_pk_id = response_video_list["data"]["list"][0]["propertyMarkId"]
        print("视频状态：", str(video_status))
        if video_status == 0:
            value_video_review = {
                "cityCode": self.data["X-City-Code"],
                "pkId": video_pk_id,
                "propertyId": property_id,
                "status": "1",
                "operateRemarks": "这是视频审核备注",
                "propertyCategory": property_category
            }

            video_review_response = request_method.RequestMethod.post_method(
                self.domain + "", token, value_video_review).json()
            print("视频审核：", str(video_review_response))

    def new_attorney_form(self, property_id, trans_type, property_category):
        """
        新增委托书标记
        :param property_id: 房源码
        :param trans_type: 租售类型，1.二手房；2.租房；
        :param property_category: 房源类型：1.住宅，2.别墅，3.商住两用，4.车位，5.商铺，6.写字楼,7.厂房,8.土地；
        :return:
        """

        token = get_header.set_token()

        attorney_form_type = ""
        if trans_type == 1:
            attorney_form_type = "sale"
        elif trans_type == 2:
            attorney_form_type = "rent"

        # 委托书编号
        attorney_form_no = attorney_form_type + "_wts_" + ''.join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(7)]) + "_" + str(
            round(time.time() * 1000))

        get_agent_list_value = {"auditStatus": 1, "agentEnabled": 1, "pageSize": 20, "pageNo": 1}
        get_agent_list_response = request_method.RequestMethod.post_method(
            self.domain + "", token, get_agent_list_value).json()
        agent_list = get_agent_list_response["data"]["list"]
        agent_id = agent_list[random.randint(0, len(agent_list)-1)]["agentId"]

        # 委托书图片
        other = []
        for i in range(4):
            url = file_upload.Upload(self.data["domain"]).upload_picture("other", 1)
            other.append(url.split("?")[0])

        new_attorney_form_value = {
            "agentId": agent_id,
            "authorizationCode": attorney_form_no,
            "estateId": self.data["estate_code"],
            "files": [
                {
                    "isCover": False,
                    "size": 0,
                    "type": "authorization",
                    "url": other[0]
                }
            ],
            "otherPics": [
                {
                    "isCover": False,
                    "size": 0,
                    "type": "authorizationOther",
                    "url": other[1]
                }
            ],
            "propertyCardNo": random.randint(111111, 999999),
            "propertyCardPics": [
                {
                    "isCover": False,
                    "size": 0,
                    "type": "authorizationPropCard",
                    "url": other[2]
                }
            ],
            "propertyCardType": random.randint(1, 4),
            "propertyCategory": property_category,
            "propertyId": property_id,
            "propertyOwnerCardNo": self.fake.ssn(),
            "propertyOwnerCardType": "1",
            "propertyOwnerName": get_name.TestTest.create_name(),
            "propertyOwnerPics": [
                {
                    "isCover": False,
                    "size": 0,
                    "type": "authorizationPropOwnerCard",
                    "url": other[3]
                }
            ],
            "remarks": "新增委托书",
            "transType": trans_type
        }
        new_attorney_form_value = request_method.RequestMethod.post_method(
            self.domain + "", token,
            new_attorney_form_value).json()
        print("新增委托书", new_attorney_form_value)

    def attorney_form_review(self, property_id, trans_type, property_category):
        """
        委托书标记审核
        :param property_id: 房源码
        :param trans_type: 租售类型，1.二手房；2.租房；
        :param property_category: 房源类型：1.住宅，2.别墅，3.商住两用，4.车位，5.商铺，6.写字楼,7.厂房,8.土地；
        :return:
        """
        token = get_header.set_token()

        # 查询标记列表
        attorney_form_value = {
            "pageNo": 1,
            "pageSize": 1,
            "markCategory": 7,
            "estateName": self.data["estate_name"],
            "propertyId": property_id,
            "transType": trans_type
        }
        attorney_form_response = request_method.RequestMethod.post_method(
            self.domain + "", token, attorney_form_value).json()
        attorney_form_status = attorney_form_response["data"]["list"][0]["status"]
        attorney_form_id = attorney_form_response["data"]["list"][0]["propertyMarkId"]
        print("委托书状态：", str(attorney_form_status))

        if attorney_form_status == 0:
            value_video_review = {
                "cityCode": self.data["X-City-Code"],
                "pkId": attorney_form_id,
                "propertyId": property_id,
                "status": "1",
                "operateRemarks": "委托书标记审核",
                "propertyCategory": property_category
            }

            video_review_response = request_method.RequestMethod.post_method(
                self.domain + "", token, value_video_review).json()
            print("委托书审核：", str(video_review_response))
