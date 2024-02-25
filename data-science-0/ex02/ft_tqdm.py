# Loading.py


def ft_tqdm(lst: range):
    """
    This function is a clone of the tqdm library.
    It takes a range and prints a progress bar.

    Args:
        lst (range): A range of numbers.

    Returns:
        None
    """
    total = len(lst)
    bar_width = 40

    for i, _ in enumerate(lst):
        progress = (i + 1) / total
        progress_width = int(progress * bar_width)
        bar = '=' * progress_width + '>' + ' ' * (bar_width - progress_width)

        print(f'\r{progress:.0%}|{bar}| {i + 1}/{total}', end='', flush=True)

        yield i

    print()
