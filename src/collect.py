#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
# 

from os.path import abspath, join, dirname
import sys
import argparse
import subprocess

__dir__ = dirname(__file__)
sys.path.append(__dir__)

from tul.flow123d.utils.strings import random_hex
import tul.flow123d.collect.tools.loader as loader
import tul.flow123d.collect.tools.modules.flow123d_profiler as profiler


# estimate flow root
flow_root = abspath(join(__dir__, '../../Flow123d/flow123d'))


# prepare parser
parser = argparse.ArgumentParser('collect')
parser.add_argument('--root', metavar='FLOW_ROOT', default=flow_root)
parser.add_argument('-t', '--test', action='append', metavar='TEST')


# parse and fix list of tests
arg_options = parser.parse_args()
arg_options.test = ['int/01_square/'] if not arg_options.test else arg_options.test


# runtest wrapper
runtest = abspath(join(flow_root, 'tests/runtest'))

# prepare random variables
rnd = random_hex(8)
eq_lambda = lambda x: str(x).find(rnd) != -1

# build command
command = [runtest] + arg_options.test + '--include benchmark --no-compare --no-clean --status-file'.split()
command = command + ['--random-output-dir', rnd]
print(' '.join(command))

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
