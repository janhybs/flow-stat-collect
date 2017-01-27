#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import random


def random_hex(length=8):
    return ''.join(random.choice('0123456789ABCDEF') for i in range(length))


def pad(s:str, prefix='    | ', suffix='', join='\n') -> str:
    return join.join(['%s%s%s' % (prefix, x, suffix) for x in s.splitlines()])
