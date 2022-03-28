"""
生成手机号码
"""
import random
from faker import Faker


class Phone:

    @staticmethod
    def create_phone():
        # 随机生成手机号码，两种方式，一种为自定义组装，一种为直接使用第三方库生成
        # pre_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150",
        #             "151", "152", "153", "155", "156", "157", "158", "159", "186", "187", "188", "189"]
        # phone = random.choice(pre_list) + "".join(random.choice("0123456789") for i in range(8))
        # return phone

        fake = Faker(locale='zh_CN')
        return fake.phone_number()
