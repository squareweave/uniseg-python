from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from distutils.core import setup


setup(
    name = 'uniseg',
    version = '0.6.2',
    author = 'Masaaki Shibata',
    author_email = 'mshibata@emptypage.jp',
    url = 'https://bitbucket.org/emptypage/uniseg-python',
    description = 'A pure Python module to determine Unicode text segmentations',
    packages = ['uniseg'],
    package_data = {
        'uniseg': ['ucd.sqlite3'],
    },
    scripts = ['unibreak.py', 'uniwrap.py', 'wxwrapdemo.py'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
    ],
)
