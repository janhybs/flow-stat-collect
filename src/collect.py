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

from tul.flow123d.utils.strings import random_hex
from tul.flow123d.common.config import cfg
import tul.flow123d.collect.tools.loader as loader
import tul.flow123d.collect.tools.modules.flow123d_profiler as profiler

default_options = '--include benchmark --no-compare --no-clean --status-file'
default_options_all = '--no-compare --no-clean --status-file'



# prepare parser
parser = argparse.ArgumentParser('collect')
parser.add_argument('--root', metavar='FLOW_ROOT')
parser.add_argument('-t', '--test', action='append', metavar='TEST')
parser.add_argument('-a', '--all', dest='opts', action='store_const', default=default_options, const=default_options_all)


# parse and fix list of tests
arg_options = parser.parse_args()
arg_options.test = ['int/01_square/'] if not arg_options.test else arg_options.test
arg_options.root = arg_options.root or cfg.get_flow123d_root()
flow_root = arg_options.root


# runtest wrapper
runtest = abspath(join(flow_root, 'tests/runtest'))

# prepare random variables
rnd = random_hex(8)
eq_lambda = lambda x: str(x).find(rnd) != -1

# build command
command = [runtest] + arg_options.test
command = command + arg_options.opts.split()
command = command + ['--random-output-dir', rnd]
command_str = ' '.join(command)

print("""
[ INFO ]  | Running:
    {command_str}
[ INFO ]  | From location:
    {flow_root}
""".format(**locals()).strip())
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
        print(result.acknowledged)
    else:
        print('[ ERROR ] | Did not found any artifacts')


# check result
print('=' * 80)
if process.returncode == 0:
    # if tests passed, we will save result to database
    print('[ OK ]    | Process ended successfully')
    load_data()
else:
    # print error on error
    print('[ ERROR ] | Error while executing command, return code %d' % process.returncode)
    sys.exit(1)
