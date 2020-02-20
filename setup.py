import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-conway",
    version="0.0.1",
    author="Brandon Satrom",
    author_email="bsatrom@gmail.com",
    description="TDD-style implementation of Conway's Game of Life in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsatrom/py-conway",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)