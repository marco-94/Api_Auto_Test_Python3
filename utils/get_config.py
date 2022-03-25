"""
获取yaml配置文件信息
"""
import yaml
import warnings
from config.set_path import CONFIG_FILE


def get_config():
    warnings.simplefilter('ignore', ResourceWarning)
    file = open(CONFIG_FILE, "r", encoding='utf-8')
    data = yaml.load(file.read(), Loader=yaml.Loader)
    return data
