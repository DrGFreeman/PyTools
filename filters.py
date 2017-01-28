import numpy as np

class Filter1D:

    def __init__(self, maxSize=3):
        try:
            if maxSize % 2 == 1 and maxSize >= 3:
                self._maxSize = maxSize
            else:
                raise ValueError
        except ValueError:
            raise ValueError("maxSize must be an odd integer >= 3")
        self._data = np.zeros(1)

    def addDataPoint(self, dataPoint):
        ##  Append new data point to end of array
        self._data = np.insert(self._data, self._data.size, dataPoint)
        ##  Trim begining begining of array if longer than maxSize
        if self._data.size > self._maxSize:
            self._data = self._data[self._data.size - self._maxSize:]

    def getData(self):
        return self._data

    def getLast(self):
        return self._data[-1]

    def getMean(self, windowSize=0):
        try:
            if type(windowSize) is int:
                if windowSize <= 0 or windowSize > self._maxSize:
                    windowSize = self._maxSize
                return np.mean(self._data[-windowSize:])
            else:
                raise TypeError
        except TypeError:
            raise TypeError("windowSize must be an integer")

    def getMedian(self, windowSize=0):
        try:
            if windowSize <= 0:
                windowSize = self._maxSize
            if windowSize % 2 == 1 and windowSize <= self._maxSize:
                return np.median(self._data[-windowSize:])
            else:
                raise ValueError
        except ValueError:
            raise ValueError("windowSize must be an odd integer <= maxSize")
