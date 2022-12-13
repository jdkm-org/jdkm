#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import configparser
import getpass
import os
import platform

from libcore.exception.config_file_parse_failed_exception import ConfigFileParseFailedException
from libcore.util.string_util import StringUtil
from libcore.exception.not_support_system_type_exception import NotSupportSystemTypeException
from libcore.exception.config_key_not_exists_exception import ConfigKeyNotExistsException
from libcore.exception.get_system_info_exception import GetSystemInfoException


class Config:
    """
    配置
    """
    __default_mirror = None
    __default_lang = "en_US"
    __default_publisher = "Oracle"

    __config = None

    __config_file_windows_tpl = "{systemRoot}\\Users\\{username}\\AppData\\Local\\jjvm\\config\\.jjvm-config.ini"
    __config_file_osx_tpl = "/Users/{username}/.jjvm/Config/.jjvm-config.ini"
    __config_file_linux_tpl = "/home/{username}/.jjvm/config/.jjvm-config.ini"

    __config_file_windows = None
    __config_file_osx = None
    __config_file_linux = None
    __curr_config_file = None

    __curr_system_type = None
    __curr_username = None
    __curr_windows_system_root = "C:"

    __allow_config_keys = (
        'mirror',
        'lang',
        'publisher'
    )

    def __init_system_info(self):
        """
        获取操作系统各种信息
        :return:
        """
        system_type = platform.system()
        curr_username = getpass.getuser()

        if StringUtil.is_empty(curr_username):
            raise GetSystemInfoException("Failed to get the current login username")

        self.__curr_username = curr_username.strip()

        if system_type == "Darwin":
            self.__curr_system_type = "OSX"
        elif system_type == "Windows":
            system_root = os.getenv("SystemDrive", default="C:")
            if StringUtil.is_empty(system_root):
                raise GetSystemInfoException("Illegal system root drive letter")
            self.__curr_windows_system_root = system_root.strip()
            self.__curr_system_type = "Windows"
        elif system_type == "Linux":
            self.__curr_system_type = "Linux"
        else:
            raise NotSupportSystemTypeException("Unsupported OS type.")

    def __init_config_file_location(self):
        """
        初始化配置文件位置
        :return:
        """
        if self.__curr_system_type == "OSX":
            self.__config_file_osx = self.__config_file_osx_tpl.format(username=self.__curr_username)
            self.__curr_config_file = self.__config_file_osx
        elif self.__curr_system_type == "Windows":
            self.__config_file_windows = self.__config_file_windows_tpl.format(
                systemRoot=self.__curr_windows_system_root,
                username=self.__curr_username)
            self.__curr_config_file = self.__config_file_windows
        elif self.__curr_system_type == "Linux":
            self.__config_file_linux = self.__config_file_linux_tpl(username=self.__curr_username)
            self.__curr_config_file = self.__config_file_linux

    def load_config_file(self):
        """
        加载配置文件
        如果文件不存在,那么不加载
        如果第一次保存配置的时候,文件不存在,直接创建
        如果文件存在,加载,修改
        :return:
        """
        # 通过操作系统路径加载配置文件 .jjvm-config.ini
        filename = self.__curr_config_file
        if os.path.exists(filename):
            self.__config = configparser.ConfigParser()
            self.__config.read(filename, encoding="utf-8")

            sections = self.__config.sections()

            if "app" not in sections:
                raise ConfigFileParseFailedException(f"Configuration file parsing exception: {filename}")

    def __init__(self):
        self.__init_system_info()
        self.__init_config_file_location()
        self.load_config_file()

    def get(self, key: str) -> str:
        """
        获取配置项
        :param key: Key
        :return: Value
        """

        if StringUtil.is_empty(key):
            raise ConfigKeyNotExistsException("{} is not in config file,because key is empty".format(key))

        key = key.strip()

        if key not in self.__allow_config_keys:
            raise ConfigKeyNotExistsException("{} is not in config file,the specified key is invalid".format(key))

        if self.__config is None:
            return self.__match_config_key(key)
        else:
            val = self.__config.get("app", key).strip()
            return self.__match_config_key(key) if StringUtil.is_empty(val) else val

    def __match_config_key(self, key: str) -> str:
        if key == "mirror":
            return self.__default_mirror
        elif key == "lang":
            return self.__default_lang
        elif key == "publisher":
            return self.__default_publisher

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
        获取配置项,如果这个配置项的值为空,返回用户设置的default
        :param key: Key
        :param default: 用户指定的默认值
        :return: Value
        """
        pass


if __name__ == '__main__':
    pass
