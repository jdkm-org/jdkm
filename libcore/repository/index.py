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
    1. 用于访问 GitHub 存储库或者镜像源的 index.json 文件。
    """

    __suffix_url = "/index.json"    # url 后缀
    __mirror = ""   # 镜像url
    __index_url = ""    # 镜像默认主页url
    __version_url_tpl = "/apps/{publisher}/index.json"  # 版本模板 url
    __apps_url_tpl = "/apps/{publisher}/versions/{version}.json"
    __apps: list[App] = None

    def __init__(self, config: Config = None):
        # TODO 根据环境变量和配置文件读取镜像源地址
        try:
            self.__mirror = config.get("mirror")
            # 处理兼容 http://mirrors.xlab.io 和 http://mirrors.xlab.io/
            if self.__mirror[-1] == '/':
                self.__mirror = self.__mirror[:-1]
            self.__index_url = self.__mirror + self.__suffix_url
        except ConfigKeyNotExistsException as e:
            raise IndexerInitFailedException("Can not read mirror from config file, because: {}".format(e))

    def __init_apps(self, app: App):
        # TODO 处理
        publisher = app.get_publisher()
        version = app.get_version()

    def get_file_response_json(self, url) -> str | None | dict:
        """
        返回指定url对应页面的内容
        """
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()

    def get_file_response_str(self, name: str, url: str) -> str | None:
        json_response = self.get_file_response_json(url)
        result = json_response[name]
        if StringUtil.is_empty(str(result)):
            return None
        return result.strip()

    def get_version(self) -> str | None:
        return self.get_file_response_str("version", self.__index_url)

    def get_name(self) -> str:
        return self.get_file_response_str("name", self.__index_url)

    def get_apps(self) -> dict:
        json_response = self.get_file_response_json(self.__index_url)
        return json_response["apps"]

    def get_publisher(self) -> tuple:
        return tuple(self.get_apps().keys())

    def get_update_time(self) -> str:
        return self.get_file_response_str("update-time", self.__index_url)

    def get_app_versions_by_publisher(self, publisher: str) -> tuple:
        json_response = self.get_file_response_json(self.__mirror + self.__version_url_tpl.format(publisher=publisher))
        return tuple(json_response.keys())

    def get_app(self, publisher: str, version: str) -> tuple:
        json_response = self.get_file_response_json(
            self.__mirror + self.__apps_url_tpl.format(publisher=publisher, version=version))
        return tuple(json_response)


if __name__ == '__main__':
    config = Config()
    index = Index(config)
    print(f"get_version: {index.get_version()}")
    print(f"get_name: {index.get_name()}")
    print(f"get_publisher: {index.get_publisher()}")
    print(f"get_update_time: {index.get_update_time()}")
    print("get_app_versions_by_publisher: {}".format(index.get_app_versions_by_publisher("oracle")))
    print("get_app: {}".format(index.get_app("oracle", "17.0.5")))
