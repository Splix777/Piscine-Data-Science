import os
import time
import functools
from contextlib import suppress
from os import path

from termcolor import colored
from logging.handlers import RotatingFileHandler
from logging import getLogger, DEBUG, StreamHandler, Formatter, Handler, addLevelName

LOG = getLogger('warehouse')
CUSTOM_MESSAGE = 15


def check_errors(on_off: bool = True) -> callable:
    """
    A decorator to catch errors in a function and print them.

    Args:
    on_off: bool
    """

    def decorator(func: callable) -> callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if on_off:
                    print(f"Error in {func.__name__}: {e}")
                    raise e
                else:
                    raise e

        return wrapper

    return decorator


def timing_decorator(msg: str = None) -> callable:
    """
    A decorator to time a function.

    Args:
    func: callable
    """

    def decorator(func: callable) -> callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            print(f'{msg}: {end_time - start_time:.2f} seconds') if msg else (
                print(f"Time taken for {func.__name__}: {end_time - start_time:.2f} seconds"))

            return result

        return wrapper

    return decorator


@check_errors(on_off=True)
def write_to_file(filename: str, data: str, method: str = 'w') -> None:
    """
        Writes data to a file.

        Args:
        filename: str
        data: str
        """
    if method not in ['w', 'a']:
        raise ValueError('Method must be "w" or "a"')
    with open(filename, method) as file:
        file.write(data)
        filesize = file.tell()
        print(f'File {filename} written, size in mb: {filesize / 1e6:.2f}')


class CustomHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def emit(self, record):
        if record.levelname == "CUSTOM":
            print_between = False
            for item in record.msg:
                with suppress(Exception):
                    if item == record.msg[0]:
                        print("-----------------------")
                    for key, value in item.items():
                        print(colored(key.ljust(9, ' '), 'blue'), colored(value, 'yellow'), sep=": ")
                    print("-----------------------")
        else:
            print(record.msg)


@check_errors(True)
def setup_logger(uuid=None, file=False):
    if not path.exists(f'{os.getcwd()}/temp_logs'):
        os.mkdir(f'{os.getcwd()}/temp_logs')
    print(f'[!] Temporary Logs Created at {os.getcwd()}/temp_logs')

    LOG.setLevel(DEBUG)
    LOG.addHandler(CustomHandler())
    addLevelName(CUSTOM_MESSAGE, "CUSTOM")
    if file and uuid:
        fh = RotatingFileHandler(path.join(os.getcwd(), 'temp_logs', uuid), maxBytes=100000, backupCount=5)
        fh.setFormatter(Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        LOG.addHandler(fh)


if __name__ == '__main__':
    setup_logger(uuid='test.log', file=True)
    LOG.log(CUSTOM_MESSAGE, [{"test": 1}, {"test2": 2}])
    LOG.debug("This is a debug message")
    LOG.info("This is an info message")
    LOG.warning("This is a warning message")
    LOG.error("This is an error message")
    LOG.critical("This is a critical message")
