#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import subprocess
import tul.flow123d.utils.strings as strings


def _run(method, cmd=None, *args, **kwargs) -> str or bool:
    """
    :type cmd: str | list
    """
    verbose = kwargs.pop('verbose', True)
    raw = kwargs.pop('raw', False)
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
        if raw:
            return result
        if not result.strip():
            result = '<no output>'
        return strings.pad(result)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        if verbose:
            print('\n'.join(['    | ' + x for x in str(e).splitlines()]))
        return False


def run(cmd=None, *args, **kwargs) -> str or bool:
    return _run(subprocess.check_output, cmd, *args, **kwargs)

