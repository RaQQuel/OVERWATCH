#!/usr/bin/env python
""" Base class for alarms.

.. code-author: Pawel Ostrowski <ostr000@interia.pl>, AGH University of Science and Technology
"""

try:
    from typing import *  # noqa
except ImportError:
    # Imports in this block below here are used solely for typing information
    from ..trending.objects.object import TrendingObject  # noqa
    from overwatch.processing.alarms.aggregatingAlarm import AggregatingAlarm  # noqa


class Alarm:
    def __init__(self, alarmText=''):
        self.alarmText = alarmText
        self.receivers = []
        self.parent = None  # type: Optional[AggregatingAlarm]

    def addReceiver(self, receiver):  # type: (callable) -> None
        self.receivers.append(receiver)

    def processCheck(self, trend=None):  # type: (Optional[TrendingObject]) -> None
        args = (trend,) if trend else ()
        result = self.checkAlarm(*args)
        isAlarm, msg = result

        if isAlarm:
            self._announceAlarm(msg)
        if self.parent:
            self.parent.childProcessed(child=self, result=isAlarm)

    def checkAlarm(self, trend):  # type: (TrendingObject) -> bool
        """abstract method"""
        raise NotImplementedError

    def _announceAlarm(self, msg):  # type: (str) -> None
        msg = "[{alarmText}]: {msg}".format(alarmText=self.alarmText, msg=msg)
        for receiver in self.receivers:
            receiver(msg)
