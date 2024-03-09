# load_from_dir.py

import os
import pandas as pd
import glob


class LoadFromDir:
    """
    A class that takes a directory with CSV files
    and loads them into a list. Performs checks
    if the directory exists and if the files are
    CSV files and other checks.

    Args:
    directory: str

    Returns:
    list
    """
    def __init__(self, directory=None, file_extension='csv', multiple_subdirectories=True):
        """
        Initializes the LoadFromDir class.
        """
        try:
            self.directory = directory
            self.file_extension = file_extension
            self.multiple_subdirectories = multiple_subdirectories
            self.filenames = []
            self.files = self.load_from_dir()
        except Exception as e:
            raise e

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def load_from_dir(self) -> list:
        """
        Loads the files from the directory into a list.

        Args:
        None

        Returns:
        list
        """
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f'The directory {self.directory} does not exist.')
        if self.multiple_subdirectories:
            files = glob.glob(self.directory + '/**/*.' + self.file_extension, recursive=True)
        else:
            files = glob.glob(self.directory + '/*.' + self.file_extension)
        if not files:
            raise FileNotFoundError(f'No files with the extension {self.file_extension} found in {self.directory}.')
        self.filenames = [os.path.basename(file).split('.')[0] for file in files]
        self.files = files
        return files
