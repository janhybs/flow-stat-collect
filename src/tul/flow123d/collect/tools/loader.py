#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import os
import fnmatch

import tul.flow123d.collect.tools.modules as modules
import tul.flow123d.collect.tools.modules.flow123d_profiler as profiler
from tul.flow123d.collect.db.mongo import Mongo
from tul.flow123d.collect.tools.modules import CollectResult


def load_data(location: str, module: modules.ICollectTool, rules: list=None):
    if not os.path.exists(location):
        raise Exception('Invalid location')

    if not os.path.isdir(location):
        location = os.path.dirname(location)

    files = recursive_glob(location, module.include)
    if rules:
        for rule in rules:
            files = [f for f in files if rule(f)]

    result = []
    for file in files:
        result.append(module.process_file(file))

    return result


def recursive_glob(root, pattern):
    results = []
    for base, dirs, files in os.walk(root):
        match = fnmatch.filter(files, pattern)
        results.extend([os.path.join(base, f) for f in match])
    return results


def save_to_database(data):
    """
    :type data: list[CollectResult]
    """
    mongo = Mongo.init()
    results = list()
    for item in data:

        # save logs first
        if item.logs and item.items:
            log_ids = mongo.fs.insert_many(item.logs).inserted_ids
            item.update(log_ids)

        # insert rest to db
        if item.items:
            results.append(mongo.flat.insert_many(item.items))
    return results
