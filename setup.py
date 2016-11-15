#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup
from setuptools.command.develop import develop

with open('README.rst') as readme_file:
    readme = readme_file.read()

class SetupDevelop(develop):
    """
        Command that sets up the development for the bacon code.
    """

    def finalize_options(self):
        # Check to make sure we are in a virtual environment before we allow this to be run.
        if not os.getenv('VIRTUAL_ENV'):
            print('ERROR: You are not in a virtual environment', sys.stderr)
            sys.exit(1)
        develop.finalize_options(self)

    def run(self):
        # Run the normal develop operations
        # Note: the develop base class is an 'old-style' class, as such super does not work.  We call
        # the super run() method the old school way.
        print('Installing development egg.')
        develop.run(self)
        print('')

        # Install the development only requirements
        print('Install development PIP dependencies.')
        self.spawn('pip install --upgrade --requirement requirements-dev.txt'.split(' '))
        print('Done installing development PIP dependencies.')


setup(
    name='arch-mirror-archive',
    version='2016.11.15',
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
    install_requires=[
        'click==4.0',
        'ipython==5.1.0'
    ],
    license="MIT",
    zip_safe=False,
    keywords='arch-mirror-archive',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass={
        'develop': SetupDevelop
    }
)
