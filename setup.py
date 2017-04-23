import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "qpost",
    version = "0.1.0",
    author = "John Parker",
    author_email = "japarker@uchicago.com",
    description = ("FDTD post-processing tools for Qbox"),
    license = "MIT",
    keywords = "FDTD",
    packages=find_packages(),
    scripts=['bin/qbox'],
    long_description=read('README.md'),
    install_requires=['h5py', 'numpy', 'scipy', 'matplotlib'],
    include_package_data = True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
    ],
)
