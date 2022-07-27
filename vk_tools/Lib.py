"""
Decorator for class Application
"""


def add_functions_as_methods(*functions):
    """
    add function
    :param functions: list of functions
    :return: decorator
    """

    def decorator(class_):
        for function in functions:
            setattr(class_, function.__name__, function)
        return class_

    return decorator


def add_function_as_methods(function):
    """
    :param function: function
    :return: decorator
    """

    def decorator(class_):
        setattr(class_, function.__name__, function)
        return class_

    return decorator
