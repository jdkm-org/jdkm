#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from libcore.util.string_util import StringUtil

from libcore.exception.config_key_not_exists_exception import ConfigKeyNotExistsException


class Config:
    """
    配置
    """

    __allow_config_keys = (
        'mirror',
        'lang',
        'publisher'
    )

    def get(self, key: str) -> str:
        """
        获取配置项
        :param key: Key
        :return: Value
        """

        if StringUtil.is_empty(key):
            raise ConfigKeyNotExistsException("{} is not in config file,because key is empty".format(key))

        if key not in self.__allow_config_keys:
            raise ConfigKeyNotExistsException("{} is not in config file,the specified key is invalid".format(key))

        ## TODO 读取配置文件

        return ""

    def set(self, key: str, value: str) -> bool:
        """
        设置配置项
        :param key: Key
        :param value: Value
        :return: 如果不存在这个配置项,那么返回 False
        """
        pass

    def get_with_default(self, key: str, default: str):
        """
        获取配置项,如果这个配置项的值为空,那么返回 default
        :param key: Key
        :param default: 默认值
        :return: Value
        """
        pass


if __name__ == '__main__':
    pass
