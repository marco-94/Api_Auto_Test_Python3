"""
房源图片集合组装
"""
import random
from interval import Interval
from utils import get_config, file_upload


class PropertyPicture:
    data = get_config.get_config()

    def __init__(self, domain):
        self.domain = domain

    def property_picture(self, picture_type, picture_number):
        """
        房源图片设置：其他图、户型图、室内图、环境图\n
        :param picture_type: 图片类型：1.其他图；2.户型图；3.室内图；4.环境图(室外图)；
        :param picture_number: 图片数量
        :return: 图片地址列表
        """
        # 判断图片数量，防止输入错误导致报错，最大可上传20张
        if picture_number not in Interval(0, 20):
            print("图片数量不正确")

        # 图片地址集合
        return_json = {
            "property_picture_list": []
        }

        # 判断需要上传的图片类型，转换成文字
        for i in range(picture_number):
            if picture_type == 1:
                picture_type = "other"

            elif picture_type == 2:
                picture_type = "houseType"

            elif picture_type == 3:
                picture_type = "indoor"

            elif picture_type == 4:
                picture_type = "environment"

            elif picture_type not in Interval(1, 4):
                print("图片类型不正确，本次不上传图片")
                break

            # 上传图片
            picture_url = file_upload.Upload(self.data["domain"]).upload_picture(picture_type, 1)

            # 判断是否设置为封面图，默认第一张为封面图
            if i == 0:
                is_cover = True
            else:
                is_cover = False

            # 拼接图片信息json
            picture = {
                "bucket": "yjyz-beta-sz",
                "name": "{}.jpg".format(i),
                "size": random.randint(100000, 150000),
                "type": picture_type,
                "url": picture_url.split("?")[0],
                "isCover": is_cover,
                "widthValid": True,
                "width": 1920,
                "height": 1080
            }

            # 把全部的图片信息json，放到图片地址集合中，并返回
            return_json["property_picture_list"].append(picture)

            # 判断需要上传的图片类型，转换成数值，用于下次循环的判断
            if picture_type == "other":
                picture_type = 1
            elif picture_type == "houseType":
                picture_type = 2
            elif picture_type == "indoor":
                picture_type = 3
            elif picture_type == "environment":
                picture_type = 4

        return return_json
