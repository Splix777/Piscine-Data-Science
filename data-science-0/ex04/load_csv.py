# load_csv.py


import os
import pandas as pd


def load(path: str) -> pd.DataFrame:
    """
    Loads a csv file into a pandas dataframe.

    Args:
    path: str

    Returns:
    pd.DataFrame
    :rtype: object
    """
    try:
        csv_shape = pd.read_csv(
            os.path.join(os.path.dirname(__file__), path)).shape
        print(f'Loading dataset of dimensions {csv_shape}')
        return pd.read_csv(os.path.join(os.path.dirname(__file__), path))
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    print(load('../subject/customer/data_2022_oct.csv'))
