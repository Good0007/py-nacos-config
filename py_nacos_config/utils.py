import os


def get_env_value(key: str, default_value=None):
    """
    读取环境变量
    :param key:
    :param default_value:
    :return:
    """
    return os.getenv(key, default_value)


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
