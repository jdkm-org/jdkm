#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from libcore.cache.cache import Cache
from libcore.config.config import Config
from libcore.exception.not_support_repository_indexer_exception import NotSupportRepositoryIndexerException
from libcore.repository.index import Index, App
from libcore.util.string_util import StringUtil


class LocalRepository:
    __indexer = None

    __file_id_tpl = "{publisher}---{version}---{os}---{arch}---{dist}"

    def __init__(self, indexer: Index):
        if indexer is None:
            raise NotSupportRepositoryIndexerException("Local Repository indexer is null.")
        self.__indexer = indexer

    def get_file_by_app(self, _app: App) -> str:
        """
        FileID: Publisher---Version---OS---Arch---Dist
        """
        file_id = Cache.get_file_by_app(self.__file_id_tpl.format(
            publisher=_app.get_publisher(),
            version=_app.get_version(),
            os=_app.get_os(),
            arch=_app.get_arch(),
            dist=_app.get_dist()
        ))

        if StringUtil.is_empty(file_id):
            return ""

        return file_id


if __name__ == '__main__':
    app = App()
    app.set_publisher("oracle")
    app.set_version("17.0.5")
    app.set_os("Windows")
    app.set_arch("x64")
    app.set_dist("zip")

    index = Index(Config())
    localRepository = LocalRepository(index)
    print(localRepository.get_file_by_app(app))

