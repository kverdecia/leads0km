#!/usr/bin/env python

"""The setup script."""
from __future__ import annotations
import os

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = open('requirements.txt').readlines()

test_requirements = open('requirements_test.txt').readlines()

setup(
    author="Karel Antonio Verdecia Ortiz",
    author_email='kverdecia@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Send leads to RunOne CRM",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='leads0km',
    name='leads0km',
    packages=find_packages(include=['leads0km', 'leads0km.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kverdecia/leads0km',
    version='0.1.1',
    zip_safe=False,
)
