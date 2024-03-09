import time
import functools


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
