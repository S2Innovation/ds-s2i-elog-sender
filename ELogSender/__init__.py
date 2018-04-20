# -*- coding: utf-8 -*-
#
# This file is part of the ELogSender project
#
# (c) by S2Innovation Sp. z o. o. [ltd.], 2018
#
# Distributed under the terms of the none license.
# See LICENSE.txt for more info.

"""PANIC-eLog integration

Integration of PANIC/PyALarm or any Tango Controls compeonents with eLog.
"""

from . import release
from .ELogSender import ELogSender, main

__version__ = release.version
__version_info__ = release.version_info
__author__ = release.author
