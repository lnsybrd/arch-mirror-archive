#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read()

setup(
    name='arch-mirror-archive',
    version='2016.11.01',
    description="System to sync Arch Linux mirrors periodicly creating versioned snapshots with btrfs",
    long_description=readme,
    author='zeroxoneb',
    author_email='zeroxoneb@gmail.com',
    url='https://github.com/zeroxoneb/arch-mirror-archive',
    packages=[
        'archarchive',
    ],
    package_dir={'archarchive':
                 'archarchive'},
    entry_points={
        'console_scripts': [
            'arch-archive = archarchive.cli:sync',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='arch-mirror-archive',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
