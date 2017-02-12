#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from os.path import abspath, join, dirname
import sys
import os
import argparse
import importlib
import subprocess

__dir__ = abspath(dirname(__file__))
__root__ = dirname(__dir__)


all_clusters = [
    'ajax', 'exmag', 'gram', 'hildor', 'luna', 'mudrc', 'tarkil'
]


def load_builder(module='pbspro'):
    """
    :rtype: tul.flow123d.collect.modules.pbspro.QSubAssembler
    """
    return importlib.import_module('tul.flow123d.collect.modules.'+module).QSubAssembler()


def main():
    sys.path.append(abspath(join(__root__, 'libs')))

    from tul.flow123d.common.config import cfg

    # prepare parser
    parser = argparse.ArgumentParser('multi-collect')
    parser.add_argument('cluster', metavar='CLUSTER', nargs='*', default=['ALL'], help="""
        Specify flow123d branch, by default '%(default)s' is used. value ALL means all clusters:
        'ajax', 'exmag', 'gram', 'hildor', 'luna', 'mudrc', 'tarkil'. Default value is ALL
    """)

    parser.add_argument('-p', '--property', metavar='NAME=VALUE', action='append', help="""
        Property which will be overridden in format -p | --property NAME=VALUE.
        Allowed NAME values are nnodes, nproc, time, mem
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
    if 'ALL' in args.cluster:
        rest = set(args.cluster) - {'ALL'}
        args.cluster = all_clusters + list(rest)

    cfg.init(dict(
        type='pbspro',
        location='/storage/praha1/home/jan-hybs/projects/Flow123dDocker/flow123d'
        )
    )

    # detect module
    module = cfg.host_config.get('type')
    module = 'pbspro'

    # set default values
    builder = load_builder(module)
    builder.time = '1:59:00'
    builder.ncpus = '2'
    builder.nnodes = '1'
    builder.script = 'python3', join(__dir__, 'collect.py'), '-f', cfg.host_config.get('location')

    # override default values
    if args.property:
        print('Global override: ')
        for prop in args.property:
            key, value = str(prop).split('=', 1)
            setattr(builder, key, value)
            print(' - {:8s} = {}'.format(key, value))
        print('-' * 60)

    if args.cluster:
        print('Generating scripts: ')
        for cluster in args.cluster:
            builder.cluster = cluster
            filename = './pbs_%s.sh' % cluster
            with open(filename, 'w') as fp:
                fp.write(builder.header)
                os.chmod(filename, 0o755)
            print('[ OK ] | qsub generated', filename)
        print('-' * 60)

    # print debug info
    print('Debug info: ')
    print('-' * 60)
    print(builder.header.rstrip())
    print('-' * 60)

    if args.cluster:
        print('Executing scripts: ')
        for cluster in args.cluster:
            builder.cluster = cluster
            filename = os.path.abspath('./pbs_%s.sh' % cluster)
            command = ['qsub', filename]
            print('[    ] | Executing', ' '.join((command)))
            process = subprocess.Popen(command)
            process.wait()
            print('[ OK ] | done')

        print('-' * 60)

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
