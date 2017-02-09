#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from os.path import abspath, join, dirname
import sys
import os
import argparse
import importlib

__dir__ = dirname(__file__)
__root__ = dirname(__dir__)


def load_builder(module='pbspro'):
    """
    :rtype: tul.flow123d.collect.modules.pbspro.QSubAssembler
    """
    return importlib.import_module('tul.flow123d.collect.modules.'+module).QSubAssembler()


def main():
    sys.path.append(abspath(join(__root__, 'libs')))

    import tul.flow123d.utils.install.flow123d as flow
    from tul.flow123d.common.config import cfg
    from tul.flow123d.csv.git import Repo

    # prepare parser
    parser = argparse.ArgumentParser('multi-collect')
    parser.add_argument('cluster', metavar='CLUSTER', nargs='+', help="""
        Specify flow123d branch, by default '%(default)s' is used.
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

    cfg.init(dict(
        type='pbspro',
        location='/storage/praha1/home/jan-hybs/projects/Flow123dDocker/flow123d'
        )
    )

    module = cfg.host_config.get('type')
    module = 'pbspro'

    builder = load_builder(module)
    builder.time = '1:00:00'
    builder.ncpus = '2'
    # builder.script = 'python3', __root__
    builder.script = 'python3', join(__root__, 'collect.py'), '-f', cfg.host_config.get('location')

    for cluster in args.cluster:
        builder.cluster = cluster
        filename = './pbs_%s.sh' % cluster
        with open(filename, 'w') as fp:
            fp.write(builder.header)
            os.chmod(filename, 0o755)
        print('qsub', filename)

    # print(builder.command)
    # print(builder.header)

    # args = parser.parse_args()
    # args.flow = args.flow or cfg.get_flow123d_root()
    # flow_root = args.flow
    # git = Repo(flow_root)
    #
    # # perform repo check and init
    # if not args.no_git:
    #     flow.check_repo(git, args.branch, args.commit)
    #
    # # run install flow123d script
    # if not args.no_install:
    #     flow.run_install(args.flow)
    #
    # # test installation
    # if not args.no_test:
    #     flow.test_installation(args.flow)

if __name__ == '__main__':
    main()
