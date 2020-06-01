#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup

_need_pytest = {'pytest', 'test'}.intersection(sys.argv)


def _read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='graphene-django-plus',
    version='2.2.3',
    author='Zerosoft Tecnologia LTDA',
    author_email='admin@zerosoft.com.br',
    description='Tools to easily create permissioned CRUD endpoints in graphene.',
    license='MIT',
    keywords=' '.join([
        'graphene',
        'django',
        'extras',
        'plus',
        'crud',
        'guardian',
        'permissions',
        'graphql',
        'query',
        'prefetch',
    ]),
    url='https://github.com/0soft/graphene-django-plus',
    packages=['graphene_django_plus'],
    setup_requires=['pytest-runner >=4.0'] if _need_pytest else [],
    long_description=_read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
    ],
)
