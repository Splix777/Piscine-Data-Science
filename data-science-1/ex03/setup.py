# setup.py
from setuptools import setup, find_packages

setup(
    name='ex03',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'jupyter',
        'pytest',
        'flake8',
        'black',
        'isort',
        'psycopg2-binary',
        'sqlalchemy',
        'python-dotenv',
    ],
)
