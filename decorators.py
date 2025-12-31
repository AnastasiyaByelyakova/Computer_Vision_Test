import time
from memory_profiler import memory_usage



def time_it(func):
    """
    A decorator to measure the execution time of a function.
    """
    def wrapper(*args, **kwargs):
        print(f"Running '{func.__name__}'...")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def memory_it(func):
    """
    A decorator to measure the peak memory usage of a function.
    """
    def wrapper(*args, **kwargs):
        mem_usage, retval = memory_usage((func, args, kwargs), retval=True, max_usage=True)
        print(f"Peak memory usage of '{func.__name__}': {mem_usage:.2f} MiB")
        return retval
    return wrapper