#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the ELogSender project
#
# (c) by S2Innovation Sp. z o. o. [ltd.], 2018
#
# Distributed under the terms of the none license.
# See LICENSE.txt for more info.
"""Contain the tests for the PANIC-eLog integration."""

# Path
import sys
import os
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.insert(0, os.path.abspath(path))

# Imports
from time import sleep
from mock import MagicMock
from PyTango import DevFailed, DevState
from devicetest import DeviceTestCase, main
from ELogSender import ELogSender

# Note:
#
# Since the device uses an inner thread, it is necessary to
# wait during the tests in order the let the device update itself.
# Hence, the sleep calls have to be secured enough not to produce
# any inconsistent behavior. However, the unittests need to run fast.
# Here, we use a factor 3 between the read period and the sleep calls.
#
# Look at devicetest examples for more advanced testing


# Device test case
class ELogSenderDeviceTestCase(DeviceTestCase):
    """Test case for packet generation."""
    # PROTECTED REGION ID(ELogSender.test_additionnal_import) ENABLED START #
    # PROTECTED REGION END #    //  ELogSender.test_additionnal_import
    device = ELogSender
    properties = {'EntryAttributes': '', 'EntryMessage': '{%0%}', 'EntryTitle': '{%1%}', 'LogbookName': '', 
                  'MaxQueueSize': '10', 'MaxQueueMessage': 'There are {%NumberOfRejectedEntries%} entries skipped to avoid flooding.', 'ArgumentsParsers': '', 'ELogCommand': 'elog', 'ELogHost': '', 'ELogPort': '80', 'ELogPath': 'logbook', 'ELogAdditionalArgs': '', }
    empty = None  # Should be []

    @classmethod
    def mocking(cls):
        """Mock external libraries."""
        # Example : Mock numpy
        # cls.numpy = ELogSender.numpy = MagicMock()
        # PROTECTED REGION ID(ELogSender.test_mocking) ENABLED START #
        # PROTECTED REGION END #    //  ELogSender.test_mocking

    def test_properties(self):
        # test the properties
        # PROTECTED REGION ID(ELogSender.test_properties) ENABLED START #
        # PROTECTED REGION END #    //  ELogSender.test_properties
        pass

    def test_State(self):
        """Test for State"""
        # PROTECTED REGION ID(ELogSender.test_State) ENABLED START #
        self.device.State()
        # PROTECTED REGION END #    //  ELogSender.test_State

    def test_Status(self):
        """Test for Status"""
        # PROTECTED REGION ID(ELogSender.test_Status) ENABLED START #
        self.device.Status()
        # PROTECTED REGION END #    //  ELogSender.test_Status

    def test_create_entry(self):
        """Test for create_entry"""
        # PROTECTED REGION ID(ELogSender.test_create_entry) ENABLED START #
        self.device.create_entry([""])
        # PROTECTED REGION END #    //  ELogSender.test_create_entry

    def test_send_entry(self):
        """Test for send_entry"""
        # PROTECTED REGION ID(ELogSender.test_send_entry) ENABLED START #
        self.device.send_entry()
        # PROTECTED REGION END #    //  ELogSender.test_send_entry

    def test_NumberOfPendingEntries(self):
        """Test for NumberOfPendingEntries"""
        # PROTECTED REGION ID(ELogSender.test_NumberOfPendingEntries) ENABLED START #
        self.device.NumberOfPendingEntries
        # PROTECTED REGION END #    //  ELogSender.test_NumberOfPendingEntries

    def test_NumberOfRejectedEntries(self):
        """Test for NumberOfRejectedEntries"""
        # PROTECTED REGION ID(ELogSender.test_NumberOfRejectedEntries) ENABLED START #
        self.device.NumberOfRejectedEntries
        # PROTECTED REGION END #    //  ELogSender.test_NumberOfRejectedEntries

    def test_TotalNumberOfRejectedEntries(self):
        """Test for TotalNumberOfRejectedEntries"""
        # PROTECTED REGION ID(ELogSender.test_TotalNumberOfRejectedEntries) ENABLED START #
        self.device.TotalNumberOfRejectedEntries
        # PROTECTED REGION END #    //  ELogSender.test_TotalNumberOfRejectedEntries


# Main execution
if __name__ == "__main__":
    main()
