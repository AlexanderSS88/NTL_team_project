def add_functions_as_methods(*functions):
    def decorator(Class):
        for function in functions:
            setattr(Class, function.__name__, function)
        return Class

    return decorator


def add_function_as_methods(function):
    def decorator(Class):
        setattr(Class, function.__name__, function)
        return Class

    return decorator
