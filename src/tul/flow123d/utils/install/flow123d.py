#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import subprocess
from os.path import abspath, join, dirname

__dir__ = abspath(dirname(__file__))
__root__ = abspath(join(__dir__, '../' * 5))

import tul.flow123d.utils.exec as exec
from tul.flow123d.csv.git import Repo


def check_repo(git:Repo, branch, commit=None):
    # 1) fetch repo latest changes
    git.fetch()
    print('-' * 80)

    # 2) switch to branch
    git.checkout(commit, branch)
    print('-' * 80)

    # 3) print repo state
    git.print_state()
    print('=' * 80)


def run_install(dir, module=None):
    print('Running install shell script')

    if module is None:
        if exec.run('which qsub', verbose=False) is False:
            module = 'local'
        else:
            module = 'pbs'
    print('Using module %s' % module)
    bin_dir = join(__root__, 'bin', module)

    # run script
    print('Executing install flow123d script')
    stream = None
    p = subprocess.Popen([join(bin_dir, 'install-flow123d.sh'), dir], stdout=stream, stderr=stream)
    p.wait()
    if p.returncode == 0:
        print('Script ended successfully')
    else:
        print('Script ended with error %d' % p.returncode)
    print('=' * 80)


def test_installation(dir):
    print('Testing flow123d installation')
    if exec.run(join(dir, 'bin/flow123d'), '--help') is False:
        print('Command ended with error!, Installation was not successful!')
    else:
        print('Installation was successful!')
    print('=' * 80)
