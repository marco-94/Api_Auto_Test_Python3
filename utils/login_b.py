"""
登录
"""
from utils import request_method, logout


class Login:
    def __init__(self, domain):
        self.domain = domain

    def get_access_token(self, username, password):

        # 最多尝试三次，如果提示“租户id或秘钥错误”，则先退出登录，再重新登录
        access_token = ""
        for _ in range(3):

            headers = {"Content-Type": "application/json"}
            authorize_params = {
                "scope": "",
                "response_type": "",
                "client_id": "",
                "redirect_url": "",
                "state": "",
                "auth_type": ""
            }
            authorize_response = request_method.RequestMethod.get_method(self.domain + "/", params1=authorize_params).json()
            code_key = authorize_response['data']['code_key']
            execute_json = {
                "c_name": "",
                "input_param": {
                    "regionCode": "86",
                    "username": username,
                    "password": password
                },
                "code_key": code_key
            }

            execute_response = request_method.RequestMethod.post_method(self.domain + "/", headers,
                                                                        execute_json).json()
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
            access_token_response = request_method.RequestMethod.post_method(self.domain + "/",
                                                                             headers, access_json).json()

            # 退出登录
            if not access_token_response['code'] == "200":
                print(access_token_response['msg'])
                logout.Logout(self.domain).log_out()
                continue
            else:
                access_token = access_token_response['data']['access_token']
                break
        return access_token

