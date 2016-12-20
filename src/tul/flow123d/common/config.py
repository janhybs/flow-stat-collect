#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from os.path import abspath, join
import fnmatch

__root__ = abspath(join(__file__, '../' * 5))


class Config(object):
    """
    Class Config is global config class
    :type _rules     : list[dict]
    """

    _rules = None
    _hostname = None
    _username = None
    _inited = None
    _root = __root__
    _default_flow123d_root = abspath(join(__root__, '../Flow123d/flow123d'))

    @classmethod
    def get_flow123d_root(cls):
        cls.init()
        for rule in cls._rules:
            host = fnmatch.fnmatch(cls._hostname, rule.get('hostname'))
            user = fnmatch.fnmatch(cls._username, rule.get('username'))

            if user and host:
                return rule.get('location')

        return cls._default_flow123d_root

    @classmethod
    def init(cls):
        if cls._inited:
            return

        import platform
        import getpass
        import yaml

        cls._inited = True
        cls._hostname = platform.node()
        cls._username = getpass.getuser()

        with open(join(cls._root, 'cfg/host_table.yaml'), 'r') as fp:
            cls._rules = yaml.load(fp)


cfg = Config
