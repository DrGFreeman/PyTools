# timedpid.py
# Source: https://github.com/DrGFreeman/PyTools
#
# MIT License
#
# Copyright (c) 2017 Julien de la Bruere-Terreault <drgfreeman@tuta.io>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This module defines a simple Proportional - Integral - Derivative (PID)
# controller with different time step calculation methods. This is a python
# implementation of my Arduino TimedPID library which can be found at
# https://github.com/DrGFreeman/TimedPID. Refer to this repository for detailed
# documentation.


import time

class TimedPID:
    # Constructor
    def __init__(self, kp = 1., ki = 0., kd = 0.):
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._cmdMin = None
        self._cmdMax = None
        self._boundRange = False
        self._errorIntegral = 0.
        self._errorPrevious = 0.
        self._lastCmdTime = time.time()

    def getCmd(self, setPoint, procVar):
        """Gets the PID command without time step.
        setPoint is the desired process set point,
        procVar is the current value of the process variable to be controlled.
        No time step is used (assumed = 1)."""

        # Calculate error terms
        error = setPoint - procVar
        self._errorIntegral += error
        errorDerivative = error - self._errorPrevious

        # Set last error to current error
        self._errorPrevious = error

        # Calculate command
        cmd = self._kp * error + self._ki * self._errorIntegral + \
            self._kd * errorDerivative

        # Return bound command
        return self._boundCmd(cmd)

    def getCmdAutoStep(self, setPoint, procVar):
        """Gets the PID command with automatic time step calculation.
        setPoint is the desired process set point,
        procVar is the current value of the process variable to be controlled,
        The time step is calculated as the time since the last call to the
        method."""

        # Calculate time step
        currentTime = time.time()
        timeStep = currentTime - self._lastCmdTime

        # Set last time method was called to current time
        self._lastCmdTime = currentTime

        # Get command
        return self.getCmdStep(setPoint, procVar, timeStep)

    def getCmdStep(self, setPoint, procVar, timeStep):
        """Gets the PID command with a specified time step.
        setPoint is the desired process set point,
        procVar is the current value of the process variable to be controlled,
        timeStep is the time step."""

        # Calculate error terms
        error = setPoint - procVar
        self._errorIntegral += (error + self._errorPrevious) / 2 * timeStep
        errorDerivative = (error - self._errorPrevious) / timeStep

        # Set last error to current error
        self._errorPrevious = error

        # Calculate command
        cmd = self._kp * error + self._ki * self._errorIntegral + \
            self._kd * errorDerivative

        # Return bound command
        return self._boundCmd(cmd)

    def setCmdRange(self, cmdMin, cmdMax):
        """Sets the maximum command range. Commands calculated outside the
        cmdMin and cmdMax will be set to cmdMin or cmdMax respectively."""
        self._cmdMin = cmdMin
        self._cmdMax = cmdMax
        self._boundRange = True

    def setGains(self, kp = 1., ki = 0., kd = 0.):
        """Sets the proportional, integral and derivative terms."""
        self._kp = kp
        self._ki = ki
        self._kd = kd

    def reset(self):
        """Resets the PID error terms and timer."""
        self._errorIntegral = 0.
        self._errorPrevious = 0.
        self._lastCmdTime = time.time()

    # Private methods

    def _boundCmd(self, cmd):
        """Bounds the command within the range _cmdMin to _cmdMax."""
        if self._boundRange:
            if cmd < self._cmdMin:
                cmd = self._cmdMin
            elif cmd > self._cmdMax:
                cmd = self._cmdMax
        return cmd
