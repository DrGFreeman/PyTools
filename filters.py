import numpy as np

class Filter1D:
    """A one dimensional filter class. Useful for real-time filtering of noisy
    time series data such as sensor signal, etc."""

    def __init__(self, maxSize=3):
        """Class constructor. maxSize argument defines the size (number of data
        points) of the signal to be kept. maxSize must be an odd integer >= 3.
        """
        try:
            if maxSize % 2 == 1 and maxSize >= 3:
                self._maxSize = maxSize
            else:
                raise ValueError
        except ValueError:
            raise ValueError("maxSize must be an odd integer >= 3")
        self._data = np.zeros(1)

    def addDataPoint(self, dataPoint):
        """Adds new data point(s) to the data array. If the data array size
        exceeds the maxSize attribute, the older data points will be trimmed
        from the array (left trim). dataPoint can be a single point, a list or
        a numpy one dimensional array."""
        ##  Append new data point(s) to end of array
        self._data = np.insert(self._data, self._data.size, dataPoint)
        ##  Trim begining begining of array if longer than maxSize
        if self._data.size > self._maxSize:
            self._data = self._data[self._data.size - self._maxSize:]

    def getData(self):
        """Returns the complete data array."""
        return self._data

    def getLast(self):
        """Returns the last (most recent) data point from the data array."""
        return self._data[-1]

    def getMean(self, windowSize=0):
        """Returns the mean of the last n points from the data array where n
        equals windowSize. If windowSize is not specified, is set to 0 or is
        greater than maxSize, windowSize will be automatically set to maxSize
        and the mean of the entire data array will be returned."""
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
        """Returns the median of the last n points from the data array where n
        equals windowSize. windowSize must be an odd integer. If windowSize
        is not specified or is set to 0, windowSize will be automatically set
        to maxSize and the median of the entire data array will be returned."""
        try:
            if windowSize <= 0:
                windowSize = self._maxSize
            if windowSize % 2 == 1 and windowSize <= self._maxSize:
                return np.median(self._data[-windowSize:])
            else:
                raise ValueError
        except ValueError:
            raise ValueError("windowSize must be an odd integer <= maxSize")
