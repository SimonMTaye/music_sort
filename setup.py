from setuptools import setup, find_packages
setup(
    name='music_sort',
    version='0.1',
    packages=find_packages(),
    description='Small Library for sorting music files',
    install_requires=['tinytag', 'fuzzywuzzy']
    )
