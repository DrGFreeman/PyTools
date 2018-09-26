import pytest
import numpy as np
from pytools.filters import Filter1D

def test_Filter1D___init__():
    # Test case of maxSize less than 3
    with pytest.raises(ValueError) as e_info:
        f = Filter1D(maxSize=1)
    # Test case of maxSize even number
    with pytest.raises(ValueError) as e_info:
        f = Filter1D(maxSize=4)
    # Test that the Filter1D object has an empty np.ndarray as ._data attribute
    f = Filter1D()
    assert type(f._data) == np.ndarray
    assert f._data.size == 0

def test_Filter1D_addDataPoint():
    f = Filter1D(maxSize=3)
    f.addDataPoint(1)
    assert f._data == np.array([1.])
    f.addDataPoint(2)
    assert np.all(f._data == np.array([1., 2.]))
    # Test truncation of _data to last 3 elements
    f.addDataPoint([3, 4])
    assert np.all(f._data == np.array([2., 3., 4.]))

def test_Filter1D_getData():
    f = Filter1D(maxSize=3)
    f.addDataPoint(np.arange(5))
    assert np.all(f.getData() == np.array([2., 3., 4.]))

def test_Filter1D_getLast():
    f = Filter1D(maxSize=3)
    f.addDataPoint(np.arange(5))
    assert np.all(f.getLast() == np.array([4.]))

def test_Filter1D_getMean():
    f = Filter1D(maxSize=5)
    # Test method call on an empty _data array
    with pytest.raises(RuntimeError):
        f.getMean()
    # Add some data
    f.addDataPoint(np.arange(5))
    # Test windowSize not an integer
    with pytest.raises(TypeError):
        f.getMean(windowSize=1.)
    # Test windowSize > maxSize => windowSize set to _maxSize
    assert f.getMean(windowSize=10) == 2.
    # Test windoSize <= 0; windowSize set to _maxSize
    assert f.getMean(windowSize=-1) == 2.
    # Test value of mean with effect of windowSize
    assert f.getMean(windowSize=3) == 3.
    # Test value of mean with windowSize=0 (default)
    assert f.getMean() == 2.

def test_Filter1D_getMedian():
    f = Filter1D(maxSize=5)
    # Test method call on an empty _data array
    with pytest.raises(RuntimeError):
        f.getMedian()
    # Add some data
    f.addDataPoint(np.arange(3, 8))
    # Test windowSize not an integer
    with pytest.raises(TypeError):
        f.getMedian(windowSize=3.)
    # Test windowSize > maxSize
    assert f.getMedian(windowSize=9) == 5.
    # Test windoSize <= 0; windoSize set to _maxSize
    assert f.getMedian(windowSize=-1) == 5.
    # Test windowSize is even
    with pytest.raises(ValueError):
        f.getMedian(windowSize=4)
    # Test value of median with effect of windowSize
    assert f.getMedian(windowSize=3) == 6.
    # Test value of median with windowSize=0 (default)
    assert f.getMedian() == 5.
