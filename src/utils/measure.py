import time


def measure_time(function, *args):
    start = time.time_ns()
    res = function(*args)
    end = time.time_ns()
    return res, end-start