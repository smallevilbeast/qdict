#!/usr/bin/env python

import os

data_files = [
    (os.path.join('share', 'applications'), ['data/qdict.desktop']),
    ]

package_data = {
    'qdict' : ['images/google.png', 'images/dict.ico', 'images/bing.png'],
    }

setup_args = {
    'name' : 'qdict',
    'version' : '0.1',
    'url': 'https://github.com/lovesnow/qdict',
    'description' : 'QDict tool',    
    'author': 'andelf',
    'maintainer': 'evilbeast',
    'maintainer_email': 'houshao55@gmail.com',
    'packages': ['qdict'],
    'scripts' : ['scripts/qdict'],
    'data_files' : data_files,
    'package_data' : package_data,
    }

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
else:
    setup_args['install_requires'] = ['pycurl']

setup(**setup_args)
