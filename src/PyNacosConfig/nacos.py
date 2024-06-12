import os

import requests
from PyNacosConfig.constants import *

"""
NacosClient is a client for Nacos server.
创建nacos客户端，用于读取nacos的配置文件
"""


def get_env_value(key: str, default_value=None):
    """
    读取环境变量
    :param key:
    :param default_value:
    :return:
    """
    return os.getenv(key, default_value)


class NacosClient:
    server_list = []

    def __init__(self, server_addr='localhost:8848', namespace='public', username='nacos', password='nacos'):
        self.server_addr = get_env_value(ENV_KEY_NACOS_SERVER_ADDR, server_addr)
        self.namespace = get_env_value(ENV_KEY_NACOS_NAMESPACE, namespace)
        self.username = get_env_value(ENV_KEY_NACOS_USERNAME, username)
        self.password = get_env_value(ENV_KEY_NACOS_PASSWORD, password)
        print(f"NacosClient init: server_addr={self.server_addr},namespace={self.namespace}")
        self.server_list = self.server_addr.split(",")

    def login(self):
        """
        登录
        curl -X POST '127.0.0.1:8848/nacos/v1/auth/login' -d 'username=nacos&password=nacos'
        返回示例
        {"accessToken":"ak","tokenTtl":18000,"globalAdmin":true}
        :return:
        """
        result = requests.post(f"http://{self.server_list[0]}/nacos/v1/auth/login",
                               data={"username": self.username, "password": self.password})
        if result.status_code == 200:
            data = result.json()
            return data["accessToken"]
        raise Exception(f"NacosClient login error: {result.text}")

    def get_nacos_config(self, data_id, group='public', tag=None, type="yaml"):
        """
        获取配置
        curl -X GET 'http://127.0.0.1:8848/nacos/v2/cs/config?dataId=nacos.example&group=DEFAULT_GROUP&namespaceId=public'

        返回示例
        {
            "code": 0,
            "message": "success",
            "data": "contentTest"
        }
        :param type: 类型 yaml/txt/json/properites
        :param tag:
        :param data_id:
        :param group:
        :return:
        """
        result = requests.get(f"http://{self.server_list[0]}/nacos/v2/cs/config",
                              params={"dataId": data_id, "group": group, "namespaceId": self.namespace, "type": type},
                              headers={"Authorization": f"Bearer {self.login()}"})
        if result.status_code == 200:
            data = result.json()
            return data["data"]
        return None


class Properties(object):
    def __init__(self, content):
        self.content = content
        self.properties = {}

    def __get_dict(self, str_name, dict_name, value):
        if str_name.find('.') > 0:
            k = str_name.split('.')[0]
            dict_name.setdefault(k, {})
            return self.__get_dict(str_name[len(k) + 1:], dict_name[k], value)
        else:
            dict_name[str_name] = value
            return

    def get_properties(self):
        lines = self.content.split('\n')
        for line in lines:
            line = line.strip().replace('\n', '')
            if line.find("#") != -1:
                line = line[0:line.find('#')]
            if line.find('=') > 0:
                strs = line.split('=')
                strs[1] = line[len(strs[0]) + 1:]
                self.__get_dict(strs[0].strip(), self.properties, strs[1].strip())
        return self.properties


class NacosConfigReader:
    config: dict
    config_content: str
    load_keywords: dict = {}

    def __init__(self, client: NacosClient, data_id, group='public', tag=None, config_type="yaml"):
        self.client = client
        self.load_keywords = {
            "data_id": get_env_value(ENV_KEY_NACOS_CONFIG_DATA_ID, data_id),
            "group": get_env_value(ENV_KEY_NACOS_CONFIG_GROUP, group),
            "tag": get_env_value(ENV_KEY_NACOS_CONFIG_TAG, None),
            "type": get_env_value(ENV_KEY_NACOS_CONFIG_TYPE, config_type)
        }
        self.config_content = self.client.get_nacos_config(**self.load_keywords)
        if self.config_content is None:
            raise Exception(f"NacosConfigReader get config error: {self.load_keywords}")

    def load_config(self, debug=False):
        _type = self.load_keywords.get("type")
        if debug:
            print("ConfigReader load config, using params:", self.load_keywords)
        if _type == 'yaml':
            import yaml
            self.config = yaml.safe_load(self.config_content)
        elif _type == 'json':
            import json
            self.config = json.loads(self.config_content)
        elif _type == 'properties' or _type == 'text':
            self.config = Properties(self.config_content).get_properties()
        else:
            raise Exception(f"not support type: {_type}")
        if debug:
            print("ConfigReader load config success:", self.config_content)
        return self.config

