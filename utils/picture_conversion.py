# -*- coding: utf-8 -*-
"""
图片转成base64
"""
import base64


class PictureConversion:
    def __init__(self, picture_path):
        self.picture_path = picture_path

    def picture_conversion_base64(self):
        with open(self.picture_path, "rb") as f:
            base64_data = base64.b64encode(f.read())
            print(str(base64_data)[2:-1])
            return str(base64_data)[2:-1]
