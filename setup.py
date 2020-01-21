#!/usr/bin/env python

from setuptools import setup, find_packages


CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Security",
    "Topic :: Security :: Cryptography",
    "Topic :: Software Development",
    "Topic :: System :: Monitoring",
]


setup(
    author="Ben Homnick",
    author_email="bhomnick@gmail.com",
    name="factom-api",
    version="1.1.1",
    description="Python client library for the Factom API",
    license="MIT License",
    platforms=["OS Independent"],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "requests>=2.20.0",
    ],
    url="https://github.com/FactomProject/factom-api",
)
