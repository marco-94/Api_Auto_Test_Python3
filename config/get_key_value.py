"""
递归查找json中key的值
"""
import json


class GetKeyValue(object):
    def __init__(self, o, mode='j'):
        self.json_object = None
        if mode == 'j':
            self.json_object = o
        elif mode == 's':
            self.json_object = json.loads(o)
        else:
            raise Exception('Unexpected mode argument.Choose "j" or "s".')

        self.result_list = []

    def search_key(self, key):
        self.result_list = []
        self.__search(self.json_object, key)
        return self.result_list

    def __search(self, json_object, key):

        for k in json_object:
            if k == key:
                self.result_list.append(json_object[k])
            if isinstance(json_object[k], dict):
                self.__search(json_object[k], key)
            if isinstance(json_object[k], list):
                for item in json_object[k]:
                    if isinstance(item, dict):
                        self.__search(item, key)
        return


gkv = GetKeyValue(o={'demo': 'show demo'}, mode='j')  # mode=j意味传入的object是一个json对象
# 也可以：
# gkv = GetKeyValue("{'demo': 'show demo'}", mode='s')  # mode=s意味着传入的object是一个json的字符串对象
# 之后，假设需要查找key=demo的值：
print(gkv.search_key('demo'))
# 就可以了。
