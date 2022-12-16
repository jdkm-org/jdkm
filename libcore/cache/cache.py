#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import platform

from libcore.config.config import Config
from libcore.exception.get_system_info_exception import GetSystemInfoException
from libcore.exception.not_support_system_type_exception import NotSupportSystemTypeException
from libcore.util.string_util import StringUtil


class Cache:
    """
    缓存,
    每次启动,扫描缓存目录
    """
    __file_ext = ".store"  # 缓存扩展名

    __curr_system_type = None
    __curr_windows_system_root = "C:"

    __cache_file_windows_tpl = "{systemRoot}\\ProgramData\\jjvmm\\cache\\"
    __cache_file_osx = "/usr/local/jjvmm/Cache/"
    __cache_file_linux = "/usr/local/jjvmm/cache/"

    __curr_config_file = None

    # __cache_name_tpl = "{fileid}####{year}#{month}#{day}{file_ext}"
    # ####{year}#{month}#{day}{file_ext}" 主要用于标记文件的下载时间,可以使用python获取文件时间的函数代替

    def __init_system_info(self):
        system_type = platform.system()
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

    def __init_cache_file_location(self):
        """
        初始化缓存文件位置
        :return:
        """
        if self.__curr_system_type == "OSX":
            self.__curr_config_file = self.__cache_file_osx
        elif self.__curr_system_type == "Windows":
            self.__curr_config_file = self.__cache_file_windows_tpl.format(systemRoot=self.__curr_windows_system_root)
        elif self.__curr_system_type == "Linux":
            self.__curr_config_file = self.__cache_file_linux

    def load_config_file(self):
        """
        初始化缓存目录, 不存在则创建
        """
        if not os.path.exists(self.__curr_config_file):
            os.makedirs(self.__curr_config_file)

    def get_curr_config_file(self):
        return self.__curr_config_file

    def __init__(self):
        config = Config()
        self.__init_system_info()
        self.__init_cache_file_location()
        self.load_config_file()


    @staticmethod
    def get_file_by_app(file_id: str, path_cache) -> str | None:
        """
        从缓存中获取文件
        FileID: Publisher---Version---OS---Arch---Dist
        CacheID = "{FileID}####{year}#{month}#{day}{file_ext}"
        """
        for _p, _d, _f in os.walk(path_cache):
            """
            _p: str 当前层的绝对路径
            _d: list 当前层的所有目录
            _f: list 当前层的所有文件
            """
            for _item in _f:
                if file_id in _item:
                    return _p + _item
        return None

    @staticmethod
    def get_store_time(name: str) -> str:
        """
        根据缓存文件名获取存储时间
        """
        return name.split("####")[1].split(".")[0].replace('#', '-')

    @staticmethod
    def get_file_id(name: str) -> str:
        """
        根据缓存文件名获取到文件ID
        """
        return name.split("####")[0]

    @staticmethod
    def scan_cache(path: str) -> tuple:
        """
        跨平台的方式扫描缓存列表
        """
        pass

    @staticmethod
    def remove_cache_name(name: str) -> bool:
        """
        删除指定的缓存
        """
        pass

    @staticmethod
    def auto_remove_cache() -> int:
        """
        删除最近30天的缓存文件
        int: 删除个数
        """
        pass

    @staticmethod
    def remove_all_caches() -> bool:
        """
        删除所有缓存
        """
        pass


if __name__ == '__main__':
    cache = Cache()
    path = "C:\\ProgramData\\jjvmm\\cache\\"
    file_items = []
    for p, d, f in os.walk(path):
        print("p", p)
        print("d", d)
        print("f", f)
        for item in f:
            file_items.append(item)


