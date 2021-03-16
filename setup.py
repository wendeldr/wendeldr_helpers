#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup
import os

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []
with open('requirements.txt') as requirements_file:
    line = requirements_file.readline()
    while line:
        line = requirements_file.readline()
        requirements.append(line)

setup(
    author="Daniel Wendelken",
    author_email='wendeldr@ucmail.uc.edu',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="Assortment of functions",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='wendeldr_helpers',
    name='wendeldr_helpers',
    packages=find_packages(include=['wendeldr_helpers', 'wendeldr_helpers.*']),
    url='https://github.com/wendeldr/wendeldr_helpers',
    version='0.1.0',
    zip_safe=False,
)
