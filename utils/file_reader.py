import yaml
import os
import random


class YamlReader:
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load后是个generator，用list组织成列表
        return self._data


class FileSearch:
    """
    获取当前目录下的文件个数和文件名
    """
    def __init__(self, file_dir):
        self.file_dir = file_dir

    def file_name(self):

        file_count = 0
        for dir_path, dir_name, file_names in os.walk(self.file_dir):
            for _ in file_names:
                file_count += 1
            files = file_names[random.randint(0, file_count-1)]
            return files
