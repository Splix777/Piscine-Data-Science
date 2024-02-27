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
    def __init__(self, directory=None, file_extension=None, multiple_subdirectories=False):
        """
        Initializes the LoadFromDir class.
        """
        try:
            self.directory = directory
            self.file_extension = file_extension
            self.multiple_subdirectories = multiple_subdirectories
            self.files = self.load_from_dir()
            self.filenames = []
        except Exception as e:
            raise e

    def load_from_dir(self) -> list:
        """
        Loads the files from the directory into a list.

        Args:
        None

        Returns:
        list
        """
        if os.path.exists(self.directory):
            if self.multiple_subdirectories:
                files = glob.glob(self.directory + '/**/*.' + self.file_extension, recursive=True)
            else:
                files = glob.glob(self.directory + '/*.' + self.file_extension)
            if len(files) == 0:
                raise FileNotFoundError(f'No files with the extension {self.file_extension} found in {self.directory}.')
            else:
                self.filenames = [file for file in files]
                self.files = files
                return files
        else:
            raise FileNotFoundError(f'The directory {self.directory} does not exist.')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../subject'))
    load = LoadFromDir(directory=full_path, file_extension='csv', multiple_subdirectories=True)
