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
    """

    def finalize_options(self):
        if not os.getenv('VIRTUAL_ENV'):
            print('ERROR: You must be in a virtual environment', sys.stderr)
            sys.exit(1)
        develop.finalize_options(self)

    def run(self):
        develop.run(self)

        # Install the dev requirements
        print('>>> Install dev requirements')
        self.spawn('pip install --upgrade --requirement requirements-dev.txt'.split(' '))
        print('<<< Instell dev requirements')


setup(
    name='btrsync',
    version='2016.11.15',
    description="Rsync + btrfs archiving utility.",
    long_description=readme,
    author='zeroxoneb',
    author_email='zeroxoneb@gmail.com',
    url='https://github.com/zeroxoneb/btrsync',
    packages=[
        'btrsync',
    ],
    package_dir={'btrsync':
                 'btrsync'},
    entry_points={
        'console_scripts': [
            'btrsync = btrsync.cli:sync',
        ]
    },
    include_package_data=True,
    install_requires=[
        'click==4.0',
    ],
    license="MIT",
    zip_safe=False,
    keywords='btrsync',
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
