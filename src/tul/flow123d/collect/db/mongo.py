#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import gridfs
from pymongo import MongoClient


class Mongo(object):
    """
    Class Mongo manages connection and queries
    :type db          : pymongo.database.Database
    :type bench       : pymongo.database.Collection
    :type nodes       : pymongo.database.Collection
    :type flat        : pymongo.database.Collection
    :type fs          : pymongo.database.Collection
    """

    _inited = False
    client = None
    db = None

    bench = None
    flat = None
    nodes = None
    fs = None

    @classmethod
    def init(cls):
        if cls._inited:
            return cls

        cls.client = MongoClient('hybs.nti.tul.cz')
        cls.db = cls.client.get_database('bench')
        cls.bench = cls.db.get_collection('bench')
        cls.nodes = cls.db.get_collection('nodes')
        cls.flat = cls.db.get_collection('flat_copy')
        cls.fs = cls.db.get_collection('fs')
        # cls.fs = gridfs.GridFS(cls.db)
        cls._inited = True
        return cls
