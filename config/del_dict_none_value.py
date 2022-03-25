"""
删除字典内value为None的键值对
"""


class DelDictNoneValue:
    def __init__(self, dict_list):
        self.dict_list = dict_list

    def del_value(self):
        new_dict_list = []
        for dict_values in self.dict_list:
            result = {key: value for key, value in dict_values.items() if value is not None}
            new_dict_list.append(result)
        return new_dict_list
