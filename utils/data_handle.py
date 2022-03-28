"""
数据处理
"""
import json


class DataHandle:
    """把数据展示给json格式化"""
    @staticmethod
    def response_json_dumps(response_json):
        return json.dumps(response_json, indent=2, sort_keys=False, ensure_ascii=False)

    @staticmethod
    def response_json_loads(response_json):
        """把json转化为字典对象"""
        return json.loads(response_json, indent=2, sort_keys=False, ensure_ascii=False)
