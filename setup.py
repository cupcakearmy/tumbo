#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'Jinja2==2.10.3',
    'PyYAML==5.4',
    'termcolor==1.1.0',
]

setup(
    name='tumbo',
    version='0.7',
    description='Matrix builder for docker',
    license="GPLv3",
    author='cupcakearmy',
    author_email='hi@nicco.io',
    url='https://github.com/cupcakearmy/tumbo',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['tumbo=tumbo.cli:cli'],
    },
    python_requires='>=3.6',
    setup_requires=requires,
    install_requires=requires,
)
