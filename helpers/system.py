import time

def track_time(func):
    """
    Decorator to track the time taken by a function and print the elapsed time.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} completed in {elapsed_time:.2f} seconds")
        return result

    return wrapper
