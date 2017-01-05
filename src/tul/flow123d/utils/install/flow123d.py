#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import subprocess
from os.path import abspath, join, dirname

__dir__ = abspath(dirname(__file__))
__root__ = abspath(join(__dir__, '../' * 5))


def _run(method, cmd=None, *args, **kwargs) -> str or bool:
    """
    :type cmd: str | list
    """
    verbose = kwargs.pop('verbose', True)
    if cmd is None:
        cmd = []

    if type(cmd) is str:
        cmd = cmd.split()

    if args:
        cmd.extend(args)
    if verbose:
        print('$ ' + ' '.join(cmd))

    try:
        result = method(cmd, stderr=subprocess.STDOUT, **kwargs).decode()
        if not result.strip():
            result = '<no output>'
        return '\n'.join(['    | ' + x for x in result.splitlines()])
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        if verbose:
            print('\n'.join(['    | ' + x for x in str(e).splitlines()]))
        return False


def run(cmd=None, *args, **kwargs) -> str or bool:
    return _run(subprocess.check_output, cmd, *args, **kwargs)


def check_repo(cwd, branch, commit=None):
    # 1) check repository
    print('Checking repository')
    result = run('git rev-parse --show-toplevel', cwd=cwd)
    if result is not False:
        print('Found repo root %s' % cwd)
    else:
        print('Repo does not exists, creating')
        result = run('git clone https://github.com/flow123d/flow123d.git', cwd)
        print(result)
    print('-' * 80)

    # 2) update
    print('Fetching repository')
    result = run('git fetch', cwd=cwd)
    print(result)
    print('-' * 80)

    # 3) switch to branch
    print('Switching to desired branch/commit')
    if commit:
        result = run('git checkout', commit, cwd=cwd)
        print(result)
    else:
        result = run('git checkout', branch, cwd=cwd)
        print(result)
        print('-' * 80)
        # checkout to latest

        # pull latest
        print('Pulling latest changes')
        result = run('git pull origin', branch, cwd=cwd)
        print(result)
        print('-' * 80)

        # checkout to branch again
        result = run('git checkout', branch, cwd=cwd)
        print(result)
    print('-' * 80)

    print('Repository is in the following state:')
    print(run('git branch', cwd=cwd))
    print(run("git log -n 1", cwd=cwd))
    print(run("git describe", cwd=cwd))

    print('=' * 80)


def run_install(dir, module=None):
    print('Running install shell script')

    if module is None:
        if run('which qsub', verbose=False) is False:
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
    if run(join(dir, 'bin/flow123d'), '--help') is False:
        print('Command ended with error!, Installation was not successful!')
    else:
        print('Installation was successful!')
    print('=' * 80)

