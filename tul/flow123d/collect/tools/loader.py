#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import os
import fnmatch
import tul.flow123d.collect.tools.modules as modules
import tul.flow123d.collect.tools.modules.flow123d_profiler as profiler
from tul.flow123d.collect.db.mongo import Mongo


def load_data(location: str, module: modules.ICollectTool, rules: list=None):
    if not os.path.exists(location):
        raise Exception('Invalid location')

    if os.path.isdir(location):
        files = recursive_glob(location, module.include)
        if rules:
            for rule in rules:
                files = [f for f in files if rule(f)]
    else:
        files = [location]

    result = []
    for file in files:
        result.extend(module.process_file(file))

    print(len(result))
    return result
    # return module.process_file(location)

def recursive_glob(root, pattern):
    results = []
    for base, dirs, files in os.walk(root):
        match = fnmatch.filter(files, pattern)
        results.extend([os.path.join(base, f) for f in match])
    return results


def save_to_database(data: list):
    mongo = Mongo.init()
    result = mongo.flat.insert_many(data)
    return result



data = load_data(
    '/home/jan-hybs/Dokumenty/Smartgit-flow/flow123d/tests',
    profiler.Flow123dProfiler(),
    [
        # lambda x: str(x).find('0C135049') != -1
    ]
)
print(save_to_database(data))