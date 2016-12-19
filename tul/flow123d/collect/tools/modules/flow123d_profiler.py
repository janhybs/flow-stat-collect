#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import os
import re
import json
import hashlib
import datetime

from tul.flow123d.collect.tools.modules import ICollectTool


class Flow123dProfiler(ICollectTool):
    include = 'profiler_info_*.log.json'
    exclude = None

    _floats = [
        re.compile('cumul-time-.+'),
        re.compile('percent'),
        re.compile('timer-resolution'),
    ]

    _ints = [
        re.compile('call-count-.+'),
        re.compile('memory-.+'),
        re.compile('file-line'),
        re.compile('task-size'),
        re.compile('run-process-count'),
    ]

    _dates = [
        re.compile('run-started-at'),
        re.compile('run-finished-at'),
    ]

    _children = 'children'

    @staticmethod
    def _parse_date(s:str) -> datetime.datetime:
        return datetime.datetime.strptime(s, '%m/%d/%y %H:%M:%S').timestamp()

    def process_file(self, f: str):
        with open(f, 'r') as fp:
            obj = json.load(fp)

        status_file = os.path.join(os.path.dirname(f), 'runtest.status.json')
        status = {}
        if os.path.exists(status_file):
            with open(status_file, 'r') as fp:
                status = json.load(fp)

        # convert fields to ints and floats
        self._convert_fields(obj, self._ints,   int)
        self._convert_fields(obj, self._floats, float)
        self._convert_fields(obj, self._dates, self._parse_date)

        # unwind
        parts = f.split('/')
        base, start = self._get_base(obj)
        base['test-name'] = parts[-4]
        base['case-name'] = parts[-2].split('.')[0]
        base.update(status)

        return self._unwind(start, list(), base)

    def _get_base(self, obj: dict) -> (dict, dict):
        if not obj or self._children not in obj:
            return {}, {}

        base = obj.copy()
        if self._children in base:
            del base[self._children]
            return base, obj[self._children][0]

    def _convert_fields(self, obj, fields, method):
        for key in obj:
            for f in fields:
                if f.match(key):
                    obj[key] = method(obj[key])

        if self._children in obj:
            for child in obj[self._children]:
                self._convert_fields(child, fields, method)

    def _unwind(self, obj: dict, result: list, base: dict = None, path: str = ''):
        item = obj.copy()
        if self._children in item:
            del item[self._children]

        tag = item['tag']
        new_path = path + '/' + tag
        indices = dict()
        indices['tag'] = tag
        indices['tag_hash'] = self._md5(tag)
        indices['path'] = new_path
        indices['path_hash'] = self._md5(new_path)
        indices['parent'] = path
        indices['parent_hash'] = self._md5(path)
        item['indices'] = indices
        item['base'] = base.copy()

        result.append(item)

        if self._children in obj:
            for o in obj[self._children]:
                self._unwind(o, result, base, new_path)
        return result

    @classmethod
    def _md5(cls, s):
        return hashlib.md5(s.encode()).hexdigest()
