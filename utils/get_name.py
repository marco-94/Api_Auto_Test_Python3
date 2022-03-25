"""
构造姓名
"""
import random
from utils import get_config


class TestTest:

    @staticmethod
    def create_name(sex=None):
        data = get_config.get_config()
        if sex is None:
            sex = random.choice(['男', '女'])
        surname = random.choice(data["surname"])
        boy_name = random.choice(data["boy-name"])
        girl_name = random.choice(data["girl-name"])
        if sex == "男":
            name = surname + boy_name
            return name
        elif sex == "女":
            name = surname + girl_name
            return name
        else:
            print("信息输入错误")
