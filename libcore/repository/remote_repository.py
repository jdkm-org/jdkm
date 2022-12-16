#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import urllib


import requests

from libcore.cache.cache import Cache
from libcore.config.config import Config
from libcore.exception.not_support_repository_indexer_exception import NotSupportRepositoryIndexerException
from libcore.repository.index import Index, App


class RemoteRepository:
    __indexer = None

    def __init__(self, indexer: Index):
        if indexer is None:
            raise NotSupportRepositoryIndexerException("Local Repository indexer is null.")
        self.__indexer = indexer

    def get_file_by_app(self, app: App):
        item = self.__indexer.get_app_single(app.get_publisher(), app.get_version(), app.get_os(), app.get_arch(),
                                             app.get_dist())
        if item:
            url = item["file"]
            path = "C:\\ProgramData\\jjvmm\\cache\\1.zip"
            # down_res = requests.get(url)
            # with open(filename, 'wb') as file:
            #     file.write(down_res.content)
            #
            start = time.time()  # 下载开始时间
            response = requests.get(url, stream=True)  # stream=True必须写上
            size = 0  # 初始化已下载大小
            chunk_size = 1024  # 每次下载的数据大小
            content_size = int(response.headers['content-length'])  # 下载文件总大小
            try:
                if response.status_code == 200:  # 判断是否响应成功
                    print('Start download,[File size]:{size:.2f} MB'.format(
                        size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
                    filepath = path
                    with open(filepath, 'wb') as file:  # 显示进度条
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            size += len(data)
                            print('\r' + '[下载进度]:%s%.2f%%' % (
                                '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
                end = time.time()  # 下载结束时间
                print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间
            except:
                print("Exception occurs in Downloading...")
        # return item


if __name__ == '__main__':
    cache = Cache()

    app = App()
    app.set_publisher("oracle")
    app.set_version("17.0.5")
    app.set_os("Windows")
    app.set_arch("x64")
    app.set_dist("zip")
    app.set_path_cache(cache.get_curr_config_file())

    index = Index(Config())
    remoteRepository = RemoteRepository(index)
    remoteRepository.get_file_by_app(app)
