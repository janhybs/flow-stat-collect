#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


class QSubAssembler(object):
    def __init__(self):
        self.time = '1:59:00'
        self.mem = '4000mb'
        self.ncpus = 1
        self.nnodes = 1
        self.cluster = None
        self.infiniband = None
        self.script = None

    @property
    def select(self):
        result = list()

        if self.nnodes:
            result.append(('select', self.nnodes))

        if self.ncpus:
            result.append(('ncpus', self.ncpus))

        if self.mem:
            result.append(('mem', self.mem))

        if self.cluster:
            result.append(('cl_'+self.cluster, 'True'))

        if self.infiniband:
            result.append(('infiniband', self.infiniband))

        joined = ''
        for r in result:
            if len(joined) == 0:
                joined += '{}={}'.format(*r)
            else:
                joined += ':{}={}'.format(*r)
        return joined

    @property
    def header(self):
        limits = []

        if self.time:
            limits.append([
                '-l', 'walltime=' + self.time
            ])

        if self.select:
            limits.append([
                '-l', self.select
            ])

            result = ['#!/bin/bash']
        for r in limits:
            result.append('#PBS ' + ' '.join(r))
        result.append('# AUTO-GENERATED SCRIPT DO NOT EDIT #')

        if self.script:
            if type(self.script) in (tuple, list):
                result.append(' '.join(self.script))
            else:
                result.append(self.script)

        result.append('')

        return '\n'.join(result)

    @property
    def command(self):
        command = ['qsub']

        if self.time:
            command.extend([
                '-l', 'walltime=' + self.time
            ])

        if self.select:
            command.extend([
                '-l', self.select
            ])

        if self.script:
            if type(self.script) in(tuple, list):
                command.append('--')
                command.extend(self.script)
            else:
                command.append(self.script)
        return command