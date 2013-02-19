#!/usr/bin/env python


from distutils.core import setup

from unicodeseg import __version__


setup(
    name = 'unicodeseg',
    version = __version__,
    author = 'Masaaki Shibata',
    author_email = 'mshibata@emptypage.jp',
    url = 'http://www.emptypage.jp/gadgets/ucd/',
    description = 'Unicode text segmentation',
    packages = ['unicodeseg'],
    package_data = {
        'unicodeseg': ['ucd.sqlite3'],
    },
    scripts = ['unibreak.py', 'uniwrap.py', 'wxwrapdemo.py'],
)
