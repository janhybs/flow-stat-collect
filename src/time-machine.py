#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from os.path import abspath, join, dirname
import sys
import argparse

__dir__ = dirname(__file__)
__root__ = dirname(__dir__)


def main():
    sys.path.append(abspath(join(__root__, 'libs')))

    import tul.flow123d.utils.strings as strings
    from tul.flow123d.common.config import cfg
    from tul.flow123d.csv.git import Repo

    # prepare parser
    parser = argparse.ArgumentParser('collect')
    parser.add_argument('-s', '--start', metavar='SHA', default='', help="""
        Specify flow123d branch, by default '%(default)s' is used.
    """)
    parser.add_argument('-f', '--flow', metavar='DIR', default=None, help="""
        Specify where will be flow123d installed.
    """)
    parser.add_argument('-e', '--end', metavar='SHA', default='', help="""
        Build specific commit which will be built.
    """)
    parser.add_argument('-l', '--limit', metavar='N', type=int, default=None, help="""
        Limit to last N commits
    """)

    parser.add_argument('--no-git', action='store_true', default=False, help="""
        If set, will omit repository checkout and pull.
    """)
    parser.add_argument('--hide-install', action='store_true', default=False, help="""
        If set, will redirect install to install.log
    """)
    parser.add_argument('--hide-collect', action='store_true', default=False, help="""
        If set, will redirect collect to collect.log
    """)
    parser.add_argument('rest', nargs='*', default=[], help="""
        Additional arguments passed to collect.py
    """)

    args = parser.parse_args()
    args.flow = args.flow or cfg.get_flow123d_root()
    flow_root = args.flow
    git = Repo(flow_root)


    fs = '{c[short]} | {c[email]:^20s} | {c[timestamp]} | {c[ago]:14s}'

    # perform repo check and init
    if not args.no_git:
        git.fetch()

    print('Finding commits in given range')
    commits = git.commit_range(args.start, args.end, args.limit)
    print(strings.pad('\n'.join(commits)))
    print('-' * 80)
    if not commits:
        print('No commits found')
        exit(1)
    total = len(commits)

    if total == 1:
        print('Warning: Found single commit for given range')
        print('-' * 80)
        print(fs.format(c=commits.commit_detail(0)))
    else:
        print('Performing action for commit range (%d commits in total):' % total)
        print('-' * 80)
        if total == 2:
            print(fs.format(c=commits.commit_detail(0)))
            print(fs.format(c=commits.commit_detail(-1)))

        elif total <= 5:
            size = total - 2
            plural = 's' if size > 1 else ''
            print(fs.format(c=commits.commit_detail(0)))
            print(' ' * 70)
            print('{:^70s}'.format('... +%d more commit%s ...' % (size, plural)))
            print(' ' * 70)
            print(fs.format(c=commits.commit_detail(-1)))

        elif total <= 10:
            size = total - 4
            plural = 's' if size > 1 else ''
            print(fs.format(c=commits.commit_detail(0)))
            print(fs.format(c=commits.commit_detail(1)))
            print(' ' * 70)
            print('{:^70s}'.format('... +%d more commit%s ...' % (size, plural)))
            print(' ' * 70)
            print(fs.format(c=commits.commit_detail(-2)))
            print(fs.format(c=commits.commit_detail(-1)))

        else:
            size = total - 8
            plural = 's' if size > 1 else ''
            for i in range(4):
                print(fs.format(c=commits.commit_detail(i)))
            print(' ' * 70)
            print('{:^70s}'.format('... +%d more commit%s ...' % (size, plural)))
            print(' ' * 70)
            for i in range(4):
                print(fs.format(c=commits.commit_detail(i - 4)))

    run(commits, args)


def run(commits, args):
    print('-' * 80)
    import install
    import collect
    import subprocess
    for i in range(len(commits)):
        print('State {:>3d} of {:<3d} ({})'.format(i + 1, len(commits), commits[i]))
        stdout = open('install.log', 'a+') if args.hide_install else None
        command = [
            sys.executable,
            install.__file__,
            '-c', commits[i],
        ]
        print(' '.join(command))
        process = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=stdout)
        process.wait()
        if args.hide_install:
            stdout.close()

        command = [
            sys.executable,
            collect.__file__,
        ] + args.rest
        
        print(' '.join(command))
        stdout = open('install.log', 'a+') if args.hide_install else None
        process = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=stdout)
        process.wait()

        if args.hide_collect:
            stdout.close()


if __name__ == '__main__':
    main() # 16 commits
