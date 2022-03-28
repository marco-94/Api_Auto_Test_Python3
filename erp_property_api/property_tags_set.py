"""
租售房源标签设置规则
"""
import random
import math


class PropertyTags:
    @staticmethod
    def sale_property_tags():
        """
        二手房房源标签设置(不适用于土地和厂房)\n
        标签来源字典：ub_renthouselabel\n
        随机选择0~10个标签\n
        :return: 产权年限、是否唯一、房源标签编码列表
        """
        # 设置房源标签、产权年限、是否唯一
        sale_return_json = {
            "property_tags_list": [],
            "property_right_type": random.randint(1, 3),
            "is_sole": random.randint(0, 1)
        }

        # 第一步：根据选择产权年限和是否唯一，设定标签
        if sale_return_json["property_right_type"] == 1:
            sale_return_json["property_tags_list"].append(512)
        elif sale_return_json["property_right_type"] == 2 and sale_return_json["is_sole"] == 0:
            sale_return_json["property_tags_list"].append(8)
        elif sale_return_json["property_right_type"] == 2 and sale_return_json["is_sole"] == 1:
            sale_return_json["property_tags_list"].append(4)
        elif sale_return_json["property_right_type"] == 3 and sale_return_json["is_sole"] == 0:
            sale_return_json["property_tags_list"].append(2)
        elif sale_return_json["property_right_type"] == 3 and sale_return_json["is_sole"] == 1:
            sale_return_json["property_tags_list"].append(1)

        # 第二步：在剩下的标签组内，随机选择0~10个标签
        for _ in range(random.randint(0, 10)):
            sale_return_json["property_tags_list"].append(int(math.pow(2, random.randint(4, 18))))

        # 第三步：去掉重复标签
        sale_return_json["property_tags_list"] = list(set(sale_return_json["property_tags_list"]))

        # 第四步：非不满二时，去掉第二步加入的的标签编码512
        if 512 in sale_return_json["property_tags_list"] and not sale_return_json["property_right_type"] == 1:
            sale_return_json["property_tags_list"].remove(512)

        return sale_return_json

    @staticmethod
    def rent_property_tags():
        """
        租房房源标签设置(不适用于土地和厂房)
        标签来源字典：ub_houselabel
        随机选择0~10个标签
        :return:
        """
        rent_return_json = {
            "property_tags_list": []
        }
        # 勾选0~10个标签
        for _ in range(random.randint(0, 10)):
            rent_return_json["property_tags_list"].append(int(math.pow(2, random.randint(0, 17))))

        # 去掉重复标签
        rent_return_json["property_tags_list"] = list(set(rent_return_json["property_tags_list"]))

        return rent_return_json
