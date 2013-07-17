#! /usr/bin/env python
# -*- coding: utf-8 -*-

import locale

def get_default_locale():
    language, encoding = locale.getdefaultlocale()
    return language.replace("_", "-"), encoding
