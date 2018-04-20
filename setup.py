#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the ELogSender project
#
# (c) by S2Innovation Sp. z o. o. [ltd.], 2018
#
# Distributed under the terms of the none license.
# See LICENSE.txt for more info.

import os
import sys
from setuptools import setup

setup_dir = os.path.dirname(os.path.abspath(__file__))

# make sure we use latest info from local code
sys.path.insert(0, setup_dir)

readme_filename = os.path.join(setup_dir, 'README.rst')
with open(readme_filename) as file:
    long_description = file.read()

release_filename = os.path.join(setup_dir, 'ELogSender', 'release.py')
exec(open(release_filename).read())

pack = ['ELogSender']

setup(name=name,
      version=version,
      description='Integration of PANIC/PyALarm or any Tango Controls compeonents with eLog.',
      packages=pack,
      include_package_data=True,
      test_suite="test",
      entry_points={'console_scripts':['ELogSender = ELogSender:main']},
      author='contact',
      author_email='contact at s2innovation.com',
      license='none',
      long_description=long_description,
      url='www.tango-controls.org',
      platforms="All Platforms"
      )
