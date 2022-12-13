#!/usr/bin/env python3
# -*- coding:utf-8 -*-

class Cache:
    """
    缓存,
    每次启动,扫描缓存目录
    """

    __file_ext = ".store"  # 缓存扩展名
    # __cache_name_tpl = "{fileid}####{year}#{month}#{day}{file_ext}"
    # ####{year}#{month}#{day}{file_ext}" 主要用于标记文件的下载时间,可以使用python获取文件时间的函数代替

    @staticmethod
    def get_file_by_app(file_id: str):
        """
        FileID: Publisher::Version::OS::Arch::Dist
        """
        pass

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
    pass
