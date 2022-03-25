"""
文件上传类
"""
import cv2
import urllib3
import requests
from utils import get_header, get_config, request_method, file_reader
from config.set_path import VIDEO_FILE, PICTURE_FILE


class Upload:


    data = get_config.get_config()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Referer": data["Referer"],
        "Authorization": data["authorization"],
        "Origin": data["Referer"],
        "x-organ-id": data["X-Organ-Id"],
        "x-city-code": data["X-City-Code"],
        "x-user-agent": "YJYJ-ERP/v2.5.0",
        "Host": data["Host"],
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    def __init__(self, domain):
        self.domain = domain

    def upload_picture(self, picture_type, upload_type):
        """
        上传图勘类
        :param picture_type: 图片类型
        :param upload_type: 上传类型，1-上传房源图勘，2-上传租房合同图片，3-上传二手房合同图片
        :return:
        """
        token = get_header.set_token()

        picture_ticker_value = ""
        user_dir = ""
        # 判断上传类型
        if upload_type == 1:
            user_dir = "resources/detail/picProspectingpic"
            picture_ticker_value = {"userDir": user_dir}
        elif upload_type == 2 or upload_type == 3:
            if upload_type == 2:
                user_dir = "erp/contract/rent"
            else:
                user_dir = "erp/contract/sale"
            picture_ticker_value = {
                "applyId": "0",
                "uploadSize": 1,
                "userDir": user_dir
            }

        picture_ticker_response = request_method.RequestMethod.get_method(
            self.domain + "/common.core.api/common/oss/ticker", token, picture_ticker_value).json()
        keys = picture_ticker_response["data"]["keys"][0]
        policy = picture_ticker_response["data"]["policy"]
        access_id = picture_ticker_response["data"]["accessId"]
        signature = picture_ticker_response["data"]["signature"]
        user_data = picture_ticker_response["data"]["userData"]

        picture_name = file_reader.FileSearch(PICTURE_FILE + "\\" + picture_type).file_name()

        file = {
            "file": open(PICTURE_FILE + "\\" + picture_type + "\\" + picture_name, "rb"),
            "Content-Type": "image/jpeg",
            "Content-Disposition": "form-data",
            "filename": picture_name
        }
        form_data = {
            "key": user_dir + "/" + keys + ".jpg",
            "policy": policy,
            "OSSAccessKeyId": access_id,
            "success_action_status": 200,
            "signature": signature
        }

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # 上传图片
        requests.post(url=self.data["static-domain"], data=form_data, headers=self.headers, files=file, verify=False)

        # 回调接口
        value_picture_callback = {
            "upload": [
                {
                    "key": keys,
                    "md5": "",
                    "suffix": "jpg"
                }
            ],
            "userData": user_data
        }

        response_picture_callback = request_method.RequestMethod.post_method(
            self.domain + "/common.core.api/common/oss/callback", token, value_picture_callback).json()
        url = response_picture_callback["data"][0]["fullUrl"]
        return url


    def upload_video(self, upload_type):
        """
        上传视频类
        :param upload_type: 上传类型，1-上传房源视频，2-上传小区视频
        """
        token = get_header.set_token()
        video_ticker_value = ""
        user_dir = ""
        # 判断上传类型
        if upload_type == 1:
            user_dir = "UBhouse/Videos/resources/detail/video/"
            video_ticker_value = {"userDir": user_dir}
        elif upload_type == 2:
            user_dir = "erp/neighbourhoods/video"
            video_ticker_value = {"applyId": "0", "uploadSize": 1, "userDir": user_dir}


        video_ticker_response = request_method.RequestMethod.get_method(
            self.domain + "/common.core.api/common/oss/ticker", token, video_ticker_value).json()
        keys = video_ticker_response["data"]["keys"][0]
        policy = video_ticker_response["data"]["policy"]
        access_id = video_ticker_response["data"]["accessId"]
        signature = video_ticker_response["data"]["signature"]
        user_data = video_ticker_response["data"]["userData"]

        # 随机获取目录下的任一文件名
        video_name = file_reader.FileSearch(VIDEO_FILE).file_name()

        # 返回视频第一帧(封面图)
        success, image = cv2.VideoCapture(VIDEO_FILE + "\\" + video_name).read()
        video_cover_picture = cv2.imwrite(PICTURE_FILE + "\\cover\\" + "cover_picture.jpg", image)

        file = {
            "file": open(VIDEO_FILE + "\\" + video_name, "rb"),
            "Content-Type": "video/mp4",
            "Content-Disposition": "form-data",
            "filename": video_name
        }

        # 视频上传附带的参数
        form_data = {
            "key": user_dir + keys + ".mp4",
            "policy": policy,
            "OSSAccessKeyId": access_id,
            "success_action_status": 200,
            "signature": signature
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # 上传视频
        requests.post(url=self.data["static-domain"], data=form_data, headers=self.headers, files=file, verify=False)

        # 回调接口
        value_video_callback = {
            "upload": [
                {
                    "key": keys,
                    "md5": "",
                    "suffix": "mp4"
                }
            ],
            "userData": user_data
        }

        response_video_callback = request_method.RequestMethod.post_method(
            self.domain + "/common.core.api/common/oss/callback", token, value_video_callback).json()
        url = response_video_callback["data"][0]["url"]
        full_url = response_video_callback["data"][0]["fullUrl"]
        print("视频播放地址:", full_url)
        return url, full_url, video_cover_picture

