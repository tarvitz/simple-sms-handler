#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys

py_version = sys.version_info


CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Natural Language :: English',
    'Topic :: Utilities'
]

install_requires = [
    'six',
    'requests',
    'responses'
]


if isinstance(py_version, tuple):
    if py_version < (2, 7):
        install_requires.append('importlib')


setup(
    name='simple-sms-handler',
    author='Nickolas Fox <tarvitz@blacklibrary.ru>',
    version='0.0.1a',

    author_email='tarvitz@blacklibrary.ru',
    download_url='https://github.com/tarvitz/test_tool/archive/master.zip',
    description='Just a test work, nothing serious',
    long_description='none',
    license='BSD license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=install_requires,
    packages=find_packages(exclude=['tests', 'docs', 'django_app']),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False
)
