# Copyright 2023 Engineerang <engineerang@jpodtech.com>
# SPDX-License-Identifier: Apache-2.0

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read() 

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'limerfectl',
    version = '0.0.1',
    author = 'Engineerang',
    author_email = 'engineerang@jpodtech.com',
    license = 'Apache-2.0',
    description = 'limerfectl is a webserver that allows you to configure the LimeRFE remotely over a network.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/engineerang/limeRFEctl',
    py_modules = ['limerfectl', 'app'],
    packages = find_packages(),
    install_requires = ['click', 'pyserial', 'flask', 'gunicorn'],
    python_requires='>=3.8',
    entry_points = '''
        [console_scripts]
        limerfectl=limerfectl:cli
    '''
)