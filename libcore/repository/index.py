#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import requests
from libcore.config.config import Config
from libcore.exception.config_key_not_exists_exception import ConfigKeyNotExistsException
from libcore.exception.indexer_init_failed_exception import IndexerInitFailedException
from libcore.util.string_util import StringUtil


class App:
    __publisher = None
    __version = None
    __os = None
    __arch = None
    __dist = None
    __checksum_algo = None
    __checksum_content = None
    __file = None

    def set_publisher(self, publisher: str):
        self.__publisher = publisher

    def get_publisher(self) -> str:
        return self.__publisher

    def set_version(self, version: str):
        self.__version = version

    def get_version(self) -> str:
        return self.__version

    def set_os(self, os: str):
        self.__os = os

    def get_os(self) -> str:
        return self.__os

    def set_arch(self, arch: str):
        self.__arch = arch

    def get_arch(self) -> str:
        return self.__arch

    def set_dist(self, dist: str):
        self.__dist = dist

    def get_dist(self) -> str:
        return self.__dist

    def set_checksum_algo(self, checksum_algo: str):
        self.__checksum_algo = checksum_algo

    def get_checksum_algo(self) -> str:
        return self.__checksum_algo

    def set__checksum_content(self, checksum_content: str):
        self.__checksum_content = checksum_content

    def get_checksum_content(self) -> str:
        return self.__checksum_content

    def set_file(self, file: str):
        self.__file = file

    def get_file(self) -> str:
        return self.__file


class Index:
    """
    用于访问 GitHub 存储库或者镜像源的 index.json 文件。
    """

    __index_json = "/index.json"
    __mirror_url = ""

    def __init__(self, config: Config = None):
        # TODO 根据环境变量和配置文件读取镜像源地址
        try:
            mirror = config.get("mirror")
            # 处理兼容 http://mirrors.xlab.io 和 http://mirrors.xlab.io/
            if mirror[-1] == '/':
                mirror = mirror[:-1]
            self.__mirror_url = mirror + self.__index_json
        except ConfigKeyNotExistsException as e:
            raise IndexerInitFailedException("Can not read mirror from config file, because: {}".format(e))

    def get_file_response_json(self) -> str | None | dict:
        response = requests.get(self.__mirror_url)
        if response.status_code != 200:
            return None

        return response.json()

    def get_version(self) -> str | None:

        json_response = self.get_file_response_json()

        index_version = json_response["version"]

        if StringUtil.is_empty(index_version):
            return None

        return index_version.strip()

    def get_name(self) -> str:
        json_response = self.get_file_response_json()
        name = json_response["name"]
        if StringUtil.is_empty(name):
            return None

        return name.strip()

    def get_publisher(self) -> str:
        pass

    def get_update_time(self) -> str:
        json_response = self.get_file_response_json()
        update_time = json_response["update_time"]
        if StringUtil.is_empty(update_time):
            return None
        return update_time

    def get_app_versions_by_publisher(self, publisher: str) -> tuple:
        pass

    def get_app(self, publisher: str, version: str) -> tuple:
        pass


if __name__ == '__main__':
    pass
