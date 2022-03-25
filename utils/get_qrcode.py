"""
图片、二维码逻辑
"""
import base64
import qrcode


class Pic:
    save_path = '../test_data/contract_file'

    def string_qrcode(self, string_text, picture_name):
        """
        字符串转二维码图片
        :param string_text: 字符串
        :param picture_name: 图片名称
        :return: 图片名称
        """
        img = qrcode.make(string_text)
        img.save(self.save_path + '/' + picture_name + '.jpg')
        return picture_name

    def qrcode_base64(self, picture_name):
        """
        二维码图片转base64
        :param picture_name: 图片名称
        :return: base64字符
        """
        with open(self.save_path + '/' + picture_name + '.jpg', "rb") as f:
            base64_data = str(base64.b64encode(f.read()), 'utf-8')
            return base64_data
