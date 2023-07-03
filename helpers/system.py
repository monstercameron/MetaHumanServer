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


# This is the outer decorator function. It accepts an object 'obj' that we want to pass to the function being decorated.
def insert_app(obj):

    # The decorator function accepts the function to be decorated as its argument.
    def decorator(func):

        # The wrapper function will replace the original function when the decorator is applied. It accepts any number of 
        # positional arguments (*args) and keyword arguments (**kwargs) so it can be used with any function, regardless of
        # the function's signature.
        def wrapper(*args, **kwargs):

            # Before the decorated function is called, we print a message to indicate that the object is being added to the function.
            print(f"Object: {obj} has been added to the function: {func.__name__}")

            # We call the decorated function with the object as the first argument, followed by the other arguments that were passed in. 
            # The return value of the original function is returned by the wrapper.
            return func(obj, *args, **kwargs)

        # The decorator function returns the wrapper function. It has the same name as the original function but its behavior has been modified.
        return wrapper

    # The outer decorator function returns the decorator function.
    return decorator

