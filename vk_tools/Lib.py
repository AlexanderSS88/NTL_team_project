"""
Decorator for class Application
"""
def add_functions_as_methods(*functions):
    """
    :param functions: list of functions
    :return: decorator
    """
    def decorator(Class):
        for function in functions:
            setattr(Class, function.__name__, function)
        return Class

    return decorator


def add_function_as_methods(function):
    """
    :param function: function
    :return: decorator
    """
    def decorator(Class):
        setattr(Class, function.__name__, function)
        return Class

    return decorator
