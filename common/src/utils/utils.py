import datetime
import functools
import os
import sys
import threading
import warnings


def deprecated(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(
            'Call to deprecated function {}.'.format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2
        )
        warnings.simplefilter('default', DeprecationWarning)
        return func(*args, **kwargs)
    return new_func


def exclude_keys(_dict, values):
    for value in values:
        _dict.pop(value)
    return _dict


def get_dir_files(directory):
    return os.listdir(directory if directory else '.')


def get_current_directory():
    return os.getcwd() + os.path.normpath('/')


def get_platform():
    return sys.platform


def unix_to_date(unix_timestamp):
    date = datetime.datetime.fromtimestamp(unix_timestamp)
    return date.strftime('%b %d %Y %H:%M:%S')


def asynchronous(func):
    @functools.wraps(func)
    def asynchronous_func(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    return asynchronous_func
