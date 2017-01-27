#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
# 

from os.path import abspath, join, dirname
import sys
import argparse
import subprocess

__dir__ = dirname(__file__)
__root__ = dirname(__dir__)
sys.path.append(abspath(join(__root__, 'libs')))

def main():
    from tul.flow123d.utils.strings import random_hex
    from tul.flow123d.common.config import cfg
    import tul.flow123d.collect.tools.loader as loader
    import tul.flow123d.collect.tools.modules.flow123d_profiler as profiler

    default_options = '--include benchmark --no-compare --no-clean --status-file'
    default_options_all = '--no-compare --no-clean --status-file'

    # prepare parser
    parser = argparse.ArgumentParser('collect')
    parser.add_argument('-f', '--flow', metavar='DIR', help="""
        Specify is flow123d repository. If not set valuer from cfg/host_table.yaml will be used.
        Based on username and hostname, script will try to find valid location.
    """)
    parser.add_argument('-t', '--test', action='append', metavar='TEST', help="""
        Specify which tests will be run. By default all tests under bench_data/benchmarks will be executed.
        This value can be set multiple times. Relative path are relative to flow123d repository folder.
    """)
    parser.add_argument('-a', '--all', dest='opts', action='store_const',
                        default=default_options, const=default_options_all, help="""
        If set will run all tags for all tests (by default only tests with tag 'benchmark' will used.
    """)
    parser.add_argument('-r', '--repeat', metavar='N', default=1, type=int, help="""
        Number indicating how many times will be runtest script called. Default behaviour is one time.
    """)

    # parse and fix list of tests
    arg_options = parser.parse_args()
    arg_options.test = ['bench_data/benchmarks'] if not arg_options.test else arg_options.test
    arg_options.flow = arg_options.flow or cfg.get_flow123d_root()
    flow_root = arg_options.flow

    # runtest wrapper
    runtest = abspath(join(flow_root, 'tests/runtest'))

    info_template = """
[ INFO ]  | Running:
    {command_str}
[ INFO ]  | From location:
    {flow_root}
    """.strip()

    total = 0
    for i in range(arg_options.repeat):
        if arg_options.repeat > 1:
            print("Repeat %02d/%02d" % (i+1, arg_options.repeat))

        # prepare random variables
        rnd = random_hex(8)
        eq_lambda = lambda x: str(x).find(rnd) != -1

        # build command
        command = [runtest] + arg_options.test
        command = command + arg_options.opts.split()
        command = command + ['--random-output-dir', rnd]
        command_str = ' '.join(command)

        print(info_template.format(**locals()))
        print('=' * 80)

        # run process
        process = subprocess.Popen(command, cwd=flow_root)
        process.wait()

        def load_data():
            data = list()
            for t in arg_options.test:
                items = loader.load_data(join(flow_root, t), profiler.Flow123dProfiler(), [eq_lambda])
                data.extend(items)
                print('  - Found %d items in %s' % (len(items), t))

            if data:
                print('Inserting %d items to database' % len(data))
                result = loader.save_to_database(data)
                return len(data)
            else:
                print('[ ERROR ] | Did not found any artifacts')
                return 0

        # check result
        print('=' * 80)
        if process.returncode == 0:
            # if tests passed, we will save result to database
            print('[ OK ]    | Process ended successfully')
            total += load_data()
        else:
            # print error on error
            print('[ ERROR ] | Error while executing command, return code %d' % process.returncode)
            sys.exit(1)

    print('=' * 80)
    print("Inserted total of %d documents" % total)

if __name__ == '__main__':
    main()
