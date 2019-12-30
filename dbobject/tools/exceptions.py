"""
Custom exceptions
"""


class DboException(Exception):
    """
    Base exception for this project
    """
    def __init__(self, msg):
        super().__init__(msg)


class ConfigError(DboException):
    """
    Used when a configuration value is missing, has an invalid data type, or unexpected value.
    """
    def __init__(self, msg):
        super().__init__(msg)


class ArgError(DboException):
    """
    Used when a argument passed to a function has an invalid data type or unexpected value.
    """
    def __init__(self, fun_name, param=None, passed_value=None, expected_value=None, expected_dtype=None, msg=None):
        message = f"{fun_name} received unexpected value."
        if param is not None:
            message += f"\nparam: {param}"
        if passed_value is not None:
            message += f"\nvalue passed: {passed_value}"
        if expected_value is not None:
            message += f"\nexpected value(s): {expected_value}"
        if expected_dtype is not None:
            message += f"\nexpected data type: {expected_dtype}"
        if msg is not None:
            message += f"\nMessage: {msg}"
        super().__init__(message)


class NoSuchRelation(DboException):
    """
    Used when a database relation does not exist.
    """
    def __init__(self, rel_name):
        super().__init__(msg=rel_name)