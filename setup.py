import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-conway",
    version="0.4.0",
    author="Brandon Satrom",
    author_email="bsatrom@gmail.com",
    description="TDD-style implementation of Conway's Game of Life in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsatrom/py-conway",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    python_requires='>=3.5',
)