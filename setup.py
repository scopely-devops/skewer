#!/usr/bin/env python

from setuptools import setup, find_packages

import os

requires = [
    'skew==0.9.0',
    'elasticsearch==1.1.1',
    'click==2.4',
    'pytz==2014.7'
]


setup(
    name='skewer',
    version=open(os.path.join('skewer', '_version')).read().strip(),
    description='Enumerate AWS resources and index them in ElasticSearch',
    long_description=open('README.md').read(),
    author='Mitch Garnaat',
    author_email='mitch@scopely.com',
    url='https://github.com/scopely-devops/skewer',
    scripts=['bin/skewer'],
    packages=find_packages(exclude=['tests*']),
    package_data={'skewer': ['_version', 'skewer-es-template.json']},
    package_dir={'skewer': 'skewer'},
    install_requires=requires,
    license=open("LICENSE").read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
)
