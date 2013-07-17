#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

root_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

def get_path(*subpath_elements, **kwargs):
    # check_exists = kwargs.get("check_exists", True)
    subpath = os.path.join(*subpath_elements)
    path = os.path.join(root_dir, subpath)
    return path

def get_icon(name):
    return  get_path("data", name)
