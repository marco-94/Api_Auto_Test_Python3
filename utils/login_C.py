"""
登录
"""
from utils import request_method


class Login:
    def __init__(self, domain):
        self.domain = domain

    def get_access_token(self, username, password):

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
                "decrypt": "",
                "state": "n",
                "username": username,
                "password": password
            },
            "code_key": code_key
        }
        execute_response = request_method.RequestMethod.post_method(self.domain + "", headers, execute_json).json()
        code = execute_response['data']['code']
        state = execute_response['data']['state']
        user_id = execute_response['data']['userId']
        access_json = {
            "client_id": "",
            "client_secret": "",
            "code": code,
            "state": state,
            "userId": user_id,
            "userIdStr": user_id,
        }
        access_token_response = request_method.RequestMethod.post_method(self.domain + "", headers, access_json).json()
        access_token = access_token_response['data']['access_token']
        return access_token

