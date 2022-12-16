#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import configparser
import getpass
import os
import platform
import shutil

from libcore.exception.config_file_parse_failed_exception import ConfigFileParseFailedException
from libcore.exception.config_value_not_exists_exception import ConfigValueNotExistsException
from libcore.util.string_util import StringUtil
from libcore.exception.not_support_system_type_exception import NotSupportSystemTypeException
from libcore.exception.config_key_not_exists_exception import ConfigKeyNotExistsException
from libcore.exception.get_system_info_exception import GetSystemInfoException


class Config:
    """
    配置
    """
    __default_mirror = "http://192.168.3.14/"
    __default_lang = "en_US"
    __default_publisher = "Oracle"

    __config = None

    __config_file_windows_tpl = "{systemRoot}\\Users\\{username}\\AppData\\Local\\jjvmm\\config\\.jjvm-config.ini"
    __config_file_osx_tpl = "/Users/{username}/.jjvmm/Config/.jjvm-config.ini"
    __config_file_linux_tpl = "/home/{username}/.jjvmm/config/.jjvm-config.ini"

    __config_file_sections_app = "app"

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
            self.__curr_config_file = self.__config_file_osx_tpl.format(username=self.__curr_username)
        elif self.__curr_system_type == "Windows":
            self.__curr_config_file = self.__config_file_windows_tpl.format(
                systemRoot=self.__curr_windows_system_root,
                username=self.__curr_username)
        elif self.__curr_system_type == "Linux":
            self.__curr_config_file = self.__config_file_linux_tpl(username=self.__curr_username)

    def load_config_file(self):
        """
        加载配置文件
        如果文件不存在,那么不加载
        如果第一次保存配置的时候,文件不存在,直接创建
        如果文件存在,加载,修改
        :return:
        """
        # 通过操作系统路径加载配置文件 .jjvm-config.ini
        # 默认的配置文件不存在, 则创建默认的配置文件
        if not os.path.exists(self.__curr_config_file):
            # 目录不存在则创建目录
            if not os.path.exists(self.__curr_config_file.replace(".jjvm-config.ini", '')):
                os.makedirs(self.__curr_config_file.replace(".jjvm-config.ini", ''))
            jjvm_config_ini = configparser.ConfigParser()
            jjvm_config_ini['app'] = {
                'publisher': self.__default_publisher,
                'mirror': self.__default_mirror,
                'lang': self.__default_lang
            }
            with open(self.__curr_config_file, 'w') as cfg:
                jjvm_config_ini.write(cfg)

        if os.path.exists(self.__curr_config_file):
            self.__config = configparser.ConfigParser()
            self.__config.read(self.__curr_config_file, encoding="utf-8")

            sections = self.__config.sections()

            if self.__config_file_sections_app not in sections:
                raise ConfigFileParseFailedException(f"Configuration file parsing exception: {self.__curr_config_file}")

    def __init__(self):
        self.__init_system_info()
        self.__init_config_file_location()
        self.load_config_file()

    def get_curr_system_type(self) -> str:
        """
        获取当前操作系统架构
        """
        return self.__curr_system_type

    def get(self, key: str) -> str:
        """
        获取配置项
        配置获取优先级: 当前环境变量 > 配置文件 > 默认值
        :param key: Key
        :return: Value
        """

        # TODO 配置获取优先级: 当前环境变量 > 配置文件 > 默认值

        if StringUtil.is_empty(key):
            raise ConfigKeyNotExistsException("{} is not in config file,because key is empty".format(key))

        key = key.strip()

        # TODO __allow_config_keys 元组中的 key 要和 __match_config_key() 中的key保持同步
        if key not in self.__allow_config_keys:
            raise ConfigKeyNotExistsException("{} is not in config file,the specified key is invalid".format(key))

        if self.__config is None:  # 当不存在配置文件ini, 则返回默认的配置项
            return self.__match_config_key(key)
        else:
            val = self.__config.get(self.__config_file_sections_app, key).strip()
            return self.__match_config_key(key) if StringUtil.is_empty(val) else val

    # TODO 合并 get() 、 get_with_default() 、 set() 重复代码

    def get_with_default(self, key: str, default: str) -> str:
        """
        获取配置项,如果这个配置项的值为空,返回用户设置的default
        配置获取优先级: 当前环境变量 > 配置文件 > 用户指定的默认值 > 默认值
        :param key: Key
        :param default: 用户指定的默认值
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
            val = self.__config.get(self.__config_file_sections_app, key).strip()
            return default if StringUtil.is_empty(val) else val

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
        if StringUtil.is_empty(key):
            raise ConfigKeyNotExistsException("{} is not in config file,because key is empty".format(key))

        key = key.strip()

        if key not in self.__allow_config_keys:
            raise ConfigKeyNotExistsException("{} is not in config file,the specified key is invalid".format(key))

        if StringUtil.is_empty(value):
            raise ConfigValueNotExistsException("The value of the configuration {} is empty".format(key))

        self.__config.set(self.__config_file_sections_app, key, value)
        self.__config.write(open(self.__curr_config_file), "w")
        # TODO 校验是否写入成功
        return True


if __name__ == '__main__':
    config = Config()

    env_dist = os.environ
    os.environ['JDKM_MIRROR'] = "http://192.168.3.14/"

    print(env_dist.get('PATH'))
    print(env_dist.get('JDKM_MIRROR'))

    if env_dist.get('JAVA_HOME'):
        print("java")

    if env_dist.get('JDKM_MIRROR'):
        print("jjvm")
