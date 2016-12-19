#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


class ICollectTool(object):
    """
    Class ICollectTool is abstract class for any collection tool
    """

    include = None
    exclude = None

    def process_file(self, f: str) -> list:
        raise NotImplemented('Method must be implemented')
