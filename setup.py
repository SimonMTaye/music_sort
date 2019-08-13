from setuptools import setup, find_packages
setup(
    name='music_sort', 
    version='1.0', 
    packages=find_packages(),
    description='Small Library for sorting music files',
    install_requires=['tinytag'],    
    )