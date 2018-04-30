# -*- coding: utf-8 -*-
#
# This file is part of the ELogSender project
#
# (c) by S2Innovation Sp. z o. o. [ltd.], 2018
#
# Distributed under the terms of the none license.
# See LICENSE.txt for more info.

""" PANIC-eLog integration

Integration of PANIC/PyALarm or any Tango Controls compeonents with eLog.
"""

# PyTango imports
import PyTango
from PyTango import DebugIt
from PyTango.server import run
from PyTango.server import Device, DeviceMeta
from PyTango.server import attribute, command
from PyTango.server import class_property, device_property
from PyTango import AttrQuality, DispLevel, DevState
from PyTango import AttrWriteType, PipeWriteType
# Additional import
# PROTECTED REGION ID(ELogSender.additionnal_import) ENABLED START #
import re
from threading import RLock
from subprocess import PIPE, Popen

def substitute(message, substitutions=[ [], {} ], depth=1):
    """
    Substitute `{%x%}` items in the message with values provided by substitutions
    :param message: message to be substituted
    :param substitutions: list of list and dictionary. List is used for {%number%} substitutions and dictionary for
    {%name%} substitutions
    :param depth: defines number of pass
    :return: substituted message
    """

    assert isinstance(message, str)

    if depth<1:
        return message

    substituted_message = message

    # substitute numbered substitutions
    i = 0
    for value in substitutions[0]:
        substituted_message = substituted_message.replace("{%%%d%%}" % i, value)
        i += 1
    # processing named substitutions
    for (k, value) in substitutions[1].items():
        substituted_message = substituted_message.replace("{%%%s%%}" % k, value)

    return substitute(substituted_message, substitutions, depth-1)

# PROTECTED REGION END #    //  ELogSender.additionnal_import

__all__ = ["ELogSender", "main"]


class ELogSender(Device):
    """
    Integration of PANIC/PyALarm or any Tango Controls compeonents with eLog.
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(ELogSender.class_variable) ENABLED START #

    # PROTECTED REGION END #    //  ELogSender.class_variable

    # ----------------
    # Class Properties
    # ----------------

    MaxQueueSize = class_property(
        dtype='int', default_value=10
    )

    MaxQueueMessage = class_property(
        dtype='str', default_value="There are {%NumberOfRejectedEntries%} entries skipped to avoid flooding."
    )

    ArgumentsParsers = class_property(
        dtype=('str',),
    )

    ELogCommand = class_property(
        dtype='str', default_value="elog"
    )

    ELogHost = class_property(
        dtype='str',
    )

    ELogPort = class_property(
        dtype=('int',), default_value=80
    )

    ELogPath = class_property(
        dtype='str', default_value="logbook"
    )

    ELogAdditionalArgs = class_property(
        dtype='str',
    )

    # -----------------
    # Device Properties
    # -----------------

    EntryAttributes = device_property(
        dtype=('str',),
    )

    EntryMessage = device_property(
        dtype='str', default_value="{%0%}"
    )

    EntryTitle = device_property(
        dtype='str', default_value="{%1%}"
    )

    LogbookName = device_property(
        dtype='str',
    )

    # ----------
    # Attributes
    # ----------

    NumberOfPendingEntries = attribute(
        dtype='uint',
        label="Pending entries",
        doc="Number of entries pending in a queue",
    )

    NumberOfRejectedEntries = attribute(
        dtype='uint',
        label="Rejected entries",
        doc="Number of rejected entries (not accepted in queue). "
            "This counter is reset when its value used to be logged into eLog.",
    )

    TotalNumberOfRejectedEntries = attribute(
        dtype='uint',
        label="Rejected entries",
        doc="Total number of rejected entries (not accepted in a queue) since device is started.",
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        # PROTECTED REGION ID(ELogSender.init_device) ENABLED START #

        self._entries_que = []
        self._number_of_rejected_entries = 0
        self._total_number_of_rejected_entries = 0
        self.lock = RLock()

        # PROTECTED REGION END #    //  ELogSender.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(ELogSender.always_executed_hook) ENABLED START #
        pass
        # PROTECTED REGION END #    //  ELogSender.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(ELogSender.delete_device) ENABLED START #
        pass
        # PROTECTED REGION END #    //  ELogSender.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_NumberOfPendingEntries(self):
        # PROTECTED REGION ID(ELogSender.NumberOfPendingEntries_read) ENABLED START #
        with self.lock:
            out = len(self._entries_que)

        return out
        # PROTECTED REGION END #    //  ELogSender.NumberOfPendingEntries_read

    def read_NumberOfRejectedEntries(self):
        # PROTECTED REGION ID(ELogSender.NumberOfRejectedEntries_read) ENABLED START #
        with self.lock:
            out = self._number_of_rejected_entries

        return out
        # PROTECTED REGION END #    //  ELogSender.NumberOfRejectedEntries_read

    def read_TotalNumberOfRejectedEntries(self):
        # PROTECTED REGION ID(ELogSender.TotalNumberOfRejectedEntries_read) ENABLED START #
        with self.lock:
            out = self._total_number_of_rejected_entries

        return out
        # PROTECTED REGION END #    //  ELogSender.TotalNumberOfRejectedEntries_read


    # --------
    # Commands
    # --------

    @command(
    dtype_in=('str',), 
    doc_in="List of values for entry creation. \nEach value is accessed as {%index%} in properties configuration.", 
    )
    @DebugIt()
    def create_entry(self, argin):
        # PROTECTED REGION ID(ELogSender.create_entry) ENABLED START #
        with self.lock:
            if len(self._entries_que) < self.MaxQueueSize:
                # if there is space in queue - add information to it
                self._entries_que.append({
                    "arguments": argin,
                    "substitutions": [argin, {}]
                })
                # reset counter
                self._number_of_rejected_entries = 0
                self.set_state("RUNNING")

            else:
                # the queue is full, increment counters
                self._number_of_rejected_entries += 1
                self._total_number_of_rejected_entries += 1

                # mark it at the last entry in the que
                self._entries_que[-1]["substitutions"][1].update({
                    "NumberOfRejectedEntries": str(self._number_of_rejected_entries),
                    "MaxQueMessage": substitute(
                        str(self.MaxQueueMessage),
                        [ [], {
                            "NumberOfRejectedEntries": str(self._number_of_rejected_entries),
                        }]
                    )
                })

        # PROTECTED REGION END #    //  ELogSender.create_entry

    @command(
    polling_period=3000,
    )
    @DebugIt()
    def send_entry(self):
        # PROTECTED REGION ID(ELogSender.send_entry) ENABLED START #


        # prepare command and message
        elog_command = ''
        elog_message = ''

        with self.lock:
            if len(self._entries_que) > 0:

                entry = self._entries_que[0]

                # pars arguments (find named groups)
                for i in range(0, len(self.ArgumentsParsers)):
                    # parsing
                    mo = re.match(self.ArgumentsParsers[i],entry["arguments"][i])
                    # updating substitutions with named groups
                    if mo is not None:
                        entry["substitutions"][1].update(mo.groupdict())

                # update substitutions with values from device attributes
                entry["substitutions"][1].update({
                    'NumberOfPendingEntries': str(len(self._entries_que)),
                    'NumberOfRejectedEntries': str(self._number_of_rejected_entries),
                    'TotalNumberOfRejectedEntries': str(self._total_number_of_rejected_entries)
                })

                # elog command
                elog_command = "%s -h %s -p %d -d %s -l %s" \
                               % (self.ELogCommand, self.ELogHost, self.ELogPort, self.ELogPath, self.LogbookName)

                # prepare entry attributes
                command_attributes_part = '-a'
                for attribute_line in self.EntryAttributes:
                    assert isinstance(attribute_line, str)
                    # parse the line
                    mo = re.match('(?P<attr_name>\w+)\s*=\s*(?P<attr_value>[^$]*)$',attribute_line)
                    # add attributes to command line
                    if mo is not None:
                        command_attributes_part += ' "%s=%s"' % (
                            mo.group('attr_name'),
                            substitute(mo.group('attr_value'), entry["substitutions"], 2)
                        )

                if len(command_attributes_part) > 2:
                    elog_command += ' ' + command_attributes_part + ' ' + self.ELogAdditionalArgs
                    
                elog_message = substitute(self.EntryMessage, entry["substitutions"], 2)

        # if there is entry to be sent it shell be sent:
        if len(elog_command) > 0:
            elog_process = Popen(elog_command, stdin=PIPE)
            elog_process.communicate(input=elog_message)

            # remove the message from the que
            with self.lock:
                self._entries_que.pop(0)

        # PROTECTED REGION END #    //  ELogSender.send_entry

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    # PROTECTED REGION ID(ELogSender.main) ENABLED START #
    return run((ELogSender,), args=args, **kwargs)
    # PROTECTED REGION END #    //  ELogSender.main

if __name__ == '__main__':
    main()
