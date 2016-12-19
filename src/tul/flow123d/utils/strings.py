#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import random


def random_hex(length=8):
    return ''.join(random.choice('0123456789ABCDEF') for i in range(length))