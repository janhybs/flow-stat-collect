#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from os.path import abspath, join
import fnmatch

__root__ = abspath(join(__file__, '../' * 5))


class Config(object):
    """
    Class Config is global config class
    :type _rules            : list[dict]
    :type host_config       : dict
    """

    _rules = None
    _hostname = None
    _username = None
    _inited = None
    _root = __root__
    _default_flow123d_root = abspath(join(__root__, '../Flow123d/flow123d'))
    host_config = None

    @classmethod
    def get_flow123d_root(cls):
        cls.init()
        if cls.host_config:
            return cls.host_config.get('location')

        return cls._default_flow123d_root

    @classmethod
    def init(cls, default_config=None):
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

        for rule in cls._rules:
            host = fnmatch.fnmatch(cls._hostname, rule.get('hostname'))
            user = fnmatch.fnmatch(cls._username, rule.get('username'))

            if user and host:
                cls.host_config = rule
                return

        if default_config:
            cls.host_config = default_config
            return

        raise LookupError("Cannot find rule for host %s, user %s" % (cls._hostname, cls._username))

cfg = Config
