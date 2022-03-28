"""
登录
"""
from utils import request_method, logout, password_encryption, get_config


class Login:
    data = get_config.get_config()

    def get_access_token(self, username, auth_type):

        # 最多尝试三次，如果提示“租户id或秘钥错误”，则先退出登录，再重新登录
        access_token = ""
        for _ in range(3):

            headers = {"Content-Type": "application/json"}
            authorize_params = {
                "auth_type": auth_type
            }
            authorize_response = request_method.RequestMethod().get_method(
                url=self.data["domain"] + "",
                params=authorize_params).json()
            code_key = authorize_response['data']['code_key']

            # 判断登录端，是否需要给密码加密
            if authorize_params["auth_type"] == "":
                passwords = self.data["password"]
                c_name = ""
            else:
                # 给密码加密
                public_keys = password_encryption.PasswordEncryption(self.data["domain"]).get_public_key()
                passwords = password_encryption.PasswordEncryption(self.data["domain"]).encrpt(self.data["password"],
                                                                                               public_keys)
                c_name = ""

            execute_json = {
                "c_name": c_name,
                "input_param": {
                    "regionCode": "86",
                    "username": username,
                    "password": passwords
                },
                "code_key": code_key
            }

            execute_response = request_method.RequestMethod().post_method(
                url=self.data["domain"] + "",
                headers=headers,
                json=execute_json).json()

            code = execute_response['data']['code']
            state = execute_response['data']['state']
            user_id = execute_response['data']['userId']
            access_json = {
                "client_id": "",
                "client_secret": "",
                "code": code,
                "state": state,
                "userId": user_id
            }
            access_token_response = request_method.RequestMethod().post_method(
                url=self.data["domain"] + "",
                headers=headers,
                json=access_json).json()

            # 退出登录
            if access_token_response['code'] == "400002113":
                print(access_token_response['msg'])
                logout.Logout(self.data["domain"]).log_out()
                continue
            elif access_token_response['code'] == "200":
                access_token = access_token_response['data']['access_token']
                break
        return access_token
