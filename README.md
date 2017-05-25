# PyTools

This repository contains various general use python tools split into different modules.

## Modules

* [filters](#filters) (filters.py)
* [pytools](#pytools) (pytools.py)
* [timedpid](#timedpid) (timedpid.py)
* [timer](#timer) (timer.py)

### filters
This module defines filters for data processing. This module requires [Numpy](http://www.numpy.org/).

#### Class `Filter1D`
This class defines a one dimensional (1D) filter useful for real-time smoothing of time series data such as sensor signals. The filter stores a certain number of data points defined by the `maxSize` argument passed to the `Filter1D()` contructor. As new data is added with the `.addDataPoint()` method, older data is eliminated so that the number of data points remains constant. Mean and median values of the last _n_ data points in the filter can be obtained with the `.getMean(windowSize)` and `.getMedian(windoSize)` methods where _n_ is defined by the `windoSize` argument.

* `Filter1D(maxSize=3)`  
Class constructor. `maxSize` argument defines the size (number of data points) of the signal to be kept. `maxSize` must be an odd integer >= 3. If `maxSize` is not defined, it is by default set to 3.

* `.addDataPoint(dataPoint)`  
Adds new data point(s) to the data array. If the data array size exceeds the `maxSize` attribute, the older data points will be trimmed from the array (left trim). `dataPoint` can be a single point, a list or a Numpy one dimensional ndarray.

* `.getData()`  
Returns the complete data array as a Numpy one dimensional ndarray.

* `.getLast()`  
Returns the last (most recent) data point from the data array.

* `.getMean(windowSize=0)`  
Returns the mean of the last _n_ points from the data array where _n_ is defined by the `windowSize` argument. If `windowSize` is not specified, is set to 0 or is greater than `maxSize`, `windowSize` will be automatically set to `maxSize` and the mean of the entire data array will be returned.

* `.getMedian(windowSize=0)`  
Returns the median of the last _n_ points from the data array where _n_ equals `windowSize`. `windowSize` must be an odd integer. If `windowSize` is not specified or is set to 0, `windowSize` will be automatically set to `maxSize` and the median of the entire data array will be returned.

### pytools

This module defines various useful functions.

* `.constrain(value, min, max)`  
Returns the `value` argument constrained within the range defined by the `min` and `max` arguments. If `value` is within `min` and `max`, it will be returned without modification. If `value` is smaller than `min` or greater than `max` the returned value will equal `min` or `max` respectively.

### timedpid

This module defines a simple [Proportional - Integral - Derivative (PID) controller](https://en.wikipedia.org/wiki/PID_controller) with different time step calculation methods. This is a python implementation of my Arduino TimedPID library which can be found at https://github.com/DrGFreeman/TimedPID or thru the Arduino Library Manager.

The controller features three options for time step calculation (the time step is used for integral and derivative error terms calculation):

1. Non-specified (unit) time step (`.getCmd()` method)
1. Auto time step calculation (uses time between calls to `.getCmdAutoStep()` method)
1. Defined time step (passed as argument to `.getCmdStep()` method)

#### Class `TimedPID`

* `TimedPID(kp=1.0, ki=0.0, kd=0.0)`  
Constructor: `kp`, `ki` and `kd` are the proportional, integral and derivative gains respectively.

* `.getCmd(setPoint, procVar)`  
Returns the system command. `setPoint` is the desired "target" value for the process variable being controlled. `procVar` is the current value of the process variable being controlled. This method uses unit time step for integral and derivative error terms calculation.

* `.getCmdAutoStep(setPoint, procVar)`  
Similar to `.getCmd()` method except this method automatically calculates the time step based on the time between two calls to this method. The calculated time step is in seconds units.

* `.getCmdStep(setPoint, procVar, timeStep)`  
Similar to `.getCmdAutoStep()` method except the time step is passed to the method via the `timeStep` argument. The time step can be in any units.

* `.reset()`  
Resets the PID error terms. The method also resets to the current time the time variable used by the `getCmdAutoStep` to calculate the time step.

* `.setCmdRange(cmdMin, cmdMax)`  
Sets the min and max command values that can be returned by the `.getCmd()`, `.getCmdAutoStep()` and `.getCmdStep()` methods to the range defined by the arguments `cmdMin` and `cmdMax`. Unless this method is called, the command range will not be limited.

* `.setGains(kp=1.0, ki=0.0, kd=0.0)`  
Sets the PID controller gains. `kp`, `ki` and `kd` are the proportional, integral and derivative gains respectively.

### timer  
This module defines a multi-purpose timer class. It can be used to measure elapsed time, manage time steps in loops, control execution times, etc. This module uses the Python _time_ module and all time values are in seconds units.

#### Class `Timer`

* `Timer()`  
Constructor, starts the timer at instantiation.

* `.getElapsed()`  
Returns the time elapsed since instantiation or last reset, minus the sum of paused time.

* `.isWithin(delay)`  
Returns `True` if elapsed time is within (less than) `delay` argument, `False` otherwise. This method is useful to control execution of `while` loops for a fixed time duration as shown in the example below:
```python
    t = Timer()
    while t.isWithin(5):
      # Code here will execute until 5 seconds have passed since
      # instantiation of t.
```

* `.pause()`  
Pauses the timer.

* `.resume()`  
Resumes the timer following call to `.pause()` method.

* `sleepToElapsed(delay, reset=True)`  
Sleeps until elapsed time reaches the time specified by the `delay` argument. If `reset` argument is set to `True` (default), the timer will also be reset. This method is useful to control fixed time steps in loops as shown in the example below:
```python
    t = Timer()
    while True:
        # Code to be executed
        # ...
        # Wait until a time step of 0.1 second is reached. This ensures the
        # loop will execute at fixed time steps, regardless of the code
        # execution time, provided it does not exceed the specified delay value.
        t.sleepToElapsed(0.1)
```
