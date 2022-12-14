#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from libcore.config.config import Config
from libcore.exception.indexer_init_failed_exception import IndexerInitFailedException
from libcore.exception.not_support_repository_indexer_exception import NotSupportRepositoryIndexerException
from libcore.repository.index import Index
from libcore.repository.local_repository import LocalRepository
from libcore.repository.remote_repository import RemoteRepository
from libcore.cache.cache import Cache


def jjvm():
    app_config = Config()
    cache = Cache()
    print(cache.curr_config_file)

    try:
        app_indexer = Index(config=app_config)
    except IndexerInitFailedException as e:
        print(e)
        return

    try:
        app_local_repository = LocalRepository(indexer=app_indexer)
        app_remote_repository = RemoteRepository(indexer=app_indexer)
    except (NotSupportRepositoryIndexerException,) as e:
        print(e)
        return

    auto_remove_num = Cache.auto_remove_cache()
    if auto_remove_num > 0:
        print("Auto task: {} cache files were emptied".format(auto_remove_num))


if __name__ == '__main__':
    jjvm()
