#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from os.path import abspath, join, dirname
import sys
import argparse

__dir__ = dirname(__file__)
__root__ = dirname(__dir__)
sys.path.append(abspath(join(__root__, 'libs')))

import tul.flow123d.utils.install.flow123d as flow
from tul.flow123d.common.config import cfg


# prepare parser
parser = argparse.ArgumentParser('collect')
parser.add_argument('-b', '--branch', metavar='NAME', default='master', help="""
    Specify flow123d branch, by default '%(default)s' is used.
""")
parser.add_argument('-f', '--flow', metavar='DIR', default=None, help="""
    Specify where will be flow123d installed.
""")
parser.add_argument('-c', '--commit', metavar='HASH', default=None, help="""
    Build specific commit which will be built.
""")

parser.add_argument('--no-git', action='store_true', default=False, help="""
    If set, will omit repository checkout and pull.
""")
parser.add_argument('--no-install', action='store_true', default=False, help="""
    If set, will omit installation
""")
parser.add_argument('--no-test', action='store_true', default=False, help="""
    If set, will omit installation testing
""")


args = parser.parse_args()
args.flow = args.flow or cfg.get_flow123d_root()
flow_root = args.flow


# perform repo check and init
if not args.no_git:
    flow.check_repo(args.flow, args.branch, args.commit)

# run install flow123d script
if not args.no_install:
    flow.run_install(args.flow)

# test installation
if not args.no_test:
    flow.test_installation(args.flow)




