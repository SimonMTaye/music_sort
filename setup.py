import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version="0.6.2",
    author="Simon Mulat",
    author_email="mulat.simon@gmail.com",
    description="Sort local audio files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SirPotato10000/music_sort",
    packages=["music_sort"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.4',
)