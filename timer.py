# timer.py
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

# This module defines a multi-purpose timer class. It can be used to measure
# elapsed time, manage time steps in loops, control execution times, etc.

import time

class Timer:

    def __init__(self):
        """Constructor, starts the timer at instantiation."""
        self.paused = False
        self.pauseInitTime = None
        self.pauseElapsed = 0
        self.initTime = time.time()

    def getElapsed(self):
        """Returns the time elapsed since instantiation or last reset minus sum
        of paused time."""
        if self.paused:
            return self.pauseInitTime - self.initTime - self.pauseElapsed
        else:
            return time.time() - self.initTime - self.pauseElapsed

    def isWithin(self, delay):
        """Returns True if elapsed time is within (less than) delay argument.
        This method is useful to control execution of while loops for a fixed
        time duration."""
        if self.getElapsed() < delay:
            return True
        else:
            return False

    def pause(self):
        """Pauses the timer."""
        self.pauseInitTime = time.time()
        self.paused = True

    def reset(self):
        """Resets the timer initial time to current time."""
        self.paused = False
        self.pauseInitTime = None
        self.pauseElapsed = 0
        self.initTime = time.time()

    def pause(self):
        """Pauses the timer."""
        self.pauseInitTime = time.time()
        self.paused = True

    def resume(self):
        """Resume the timer following call to .pause() method."""
        if self.paused:
            self.pauseElapsed += time.time() - self.pauseInitTime
            self.paused = False
        else:
            print("Warning: Timer.resume() called without prior call to Timer.pause()")

    def sleepToElapsed(self, delay, reset = True):
        """Sleeps until elapsed time reaches delay argument. If reset argument
        is set to True (default), the timer will also be reset. This method is
        useful to control fixed time steps in loops."""
        if self.getElapsed() < delay:
            time.sleep(delay - self.getElapsed())
        if reset:
            self.reset()
