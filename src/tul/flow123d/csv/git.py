#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import datetime
import tul.flow123d.utils.exec as exec

flow123d_repo = 'https://github.com/flow123d/flow123d.git'


class Repo(object):
    def __init__(self, location):
        self.cwd = location
        self.exists = self.repo_exists()
        print('-' * 80)

    def fetch(self):
        if not self.exists:
            self.create_repo()
        # fetch latest
        print('Fetching repository')
        result = exec.run('git fetch', cwd=self.cwd)
        print(result)
        return result

    def create_repo(self, url=flow123d_repo):
        result = exec.run('git clone ' + url, self.cwd)
        print(result)
        return result

    def repo_exists(self):
        print('Testing repository')
        result = exec.run('git rev-parse --show-toplevel', cwd=self.cwd)
        print(result)
        if result is not False:
            print('Found repo root %s' % self.cwd)
        else:
            print('Repo does not exists, will be created')

        return result is not False

    def checkout(self, commit=None, branch=None):
        print('Switching to desired branch/commit')

        if commit:
            result = exec.run('git checkout -f', commit, cwd=self.cwd)
            print(result)
        else:
            result = exec.run('git checkout -f', branch, cwd=self.cwd)
            print(result)
            print('-' * 80)

            # pull latest
            print('Pulling latest changes')
            result = exec.run('git pull origin', branch, cwd=self.cwd)
            print(result)
            print('-' * 80)

            # checkout to branch again
            result = exec.run('git checkout -f', branch, cwd=self.cwd)
            print(result)
        return result

    def print_state(self):
        print('Repository is in the following state:')
        print(exec.run('git branch', cwd=self.cwd))
        print(exec.run("git log -n 1", cwd=self.cwd))
        print(exec.run("git describe", cwd=self.cwd))

    def commit_range(self, start, end, limit=None):
        if not start and not end:
            end = 'HEAD'
            dots = ''
        elif start and end:
            dots = '...'
        else:
            dots = ''

        max_count = '' if not limit else '--max-count=%d' % limit
        command = 'git rev-list {max_count} {start}{dots}{end}'.format(**locals())
        commits = [str(x).strip() for x in exec.run(command, cwd=self.cwd, raw=True).splitlines()]
        commits.reverse()
        return Commits(self, commits)


class Commits(list):
    def __init__(self, git:Repo, iterable):
        super(Commits, self).__init__(iterable)
        self.git = git
        self.details = dict()

    def _fetch_details(self, sha):
        if sha not in self.details:
            command = 'git show -s --pretty=%H,%ce,%ct,%cr,%h ' + sha
            lines = exec.run(command, cwd=self.git.cwd, verbose=False, raw=True).splitlines()
            for line in lines:
                if not str(line).strip():
                    break

                p = line.split(',')
                self.details[p[0]] = dict(
                    email=p[1],
                    timestamp=datetime.datetime.fromtimestamp(int(p[2])),
                    ago=p[3],
                    sha=p[0],
                    short=p[4]
                )

    def _fetch_all(self):
        self._fetch_details(' '.join(self))

    def commit_detail(self, index=0):
        self._fetch_details(self[index])
        return self.details[self[index]]