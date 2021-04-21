#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

tests_require = [
    "pytest>=3.6.3",
    "pytest-cov",
    "mock",
    "pytest-django>=3.3.2",
    "codecov",
    "django-filter",
    "django-guardian",
    "graphene-django-optimizer",
    "graphene-django",
    "graphene",
    "graphql-core",
]


dev_requires = [
    "black==19.10b0",
    "flake8==3.7.9",
] + tests_require


setup(
    name="graphene-django-plus",
    version="2.3.2",
    author="Zerosoft Tecnologia LTDA",
    author_email="admin@zerosoft.com.br",
    description="Tools to easily create permissioned CRUD endpoints in graphene.",
    license="MIT",
    keywords=" ".join(
        [
            "graphene",
            "django",
            "extras",
            "plus",
            "crud",
            "guardian",
            "permissions",
            "graphql",
            "query",
            "prefetch",
        ]
    ),
    url="https://github.com/0soft/graphene-django-plus",
    packages=["graphene_django_plus"],
    setup_requires=["pytest-runner"],
    tests_require=tests_require,
    extras_require={
        "test": tests_require,
        "dev": dev_requires,
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
    ],
)
