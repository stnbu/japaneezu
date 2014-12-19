# -*- coding: utf-8 -*-

from setuptools import setup

import japaneezu

# README.rst dynamically generated:
with open('README.rst', 'w') as f:
    f.write(japaneezu.__doc__)

NAME = 'japaneezu'

def read(file):
    with open(file, 'r') as f:
        return f.read().strip()

setup(
    name=NAME,
    version=read('VERSION'),
    description='A curses/console foreign language language study tool. (Currently limited to Japanese.)',
    long_description=read('README.rst'),
    author='Mike Burr',
    author_email='mburr@unintuitive.org',
    url='https://github.com/stnbu/{0}'.format(NAME),
    download_url='https://github.com/stnbu/{0}/archive/master.zip'.format(NAME),
    provides=[NAME],
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console :: Curses',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 2',
    ],
    requires=['urwid', 'urwid_utils'],
    packages=[NAME, NAME+'.ui'],
    keywords=['language', 'study', 'japanese', 'parsing'],
    test_suite='nose.collector',
    entry_points={
    'console_scripts': [
        '{0} = {0}.ui.main:main'.format(NAME),
    ],
    'gui_script': []},
)
