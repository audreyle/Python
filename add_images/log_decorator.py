def log_function(func):
    # This is the function that will actually be called when someone executes a method with a decorator
    def logged(*args, **kwargs):
        print(f"Function {func.__name__} called")
        if args:
            print(f"\twith args: {args}")
        if kwargs:
            print(f"\twith kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"\tResult --> {result}")
        return result

    return logged
