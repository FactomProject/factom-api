#!/usr/bin/env python

from setuptools import setup, find_packages


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError):
    long_description = open('README.md').read()


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Multimedia :: Graphics',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'Topic :: Security',
]


setup(
    author="Ben Homnick",
    author_email="bhomnick@gmail.com",
    name="factom-api",
    version='0.0.1',
    description="Python client library for the Factom API",
    long_description=long_description,
    license='MIT License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'requests>=2.18.4',
    ],
)
