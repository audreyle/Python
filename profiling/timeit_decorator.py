import time


def timeit(method):
    def timed(*args, **kwargs):
        # Start the timer
        start = time.time()
        # Call our function
        result = method(*args, **kwargs)
        # End the timer
        end = time.time()
        # Calculate it in ms, rounded to 2 decimal places
        total_time = round((end - start) * 1000, 2)
        print(f"Total time for {method.__name__} was {total_time}ms")
        return result

    return timed
