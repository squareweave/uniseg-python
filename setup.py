from ast import literal_eval
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


DIR_SRC = 'uniseg'
VERSION = literal_eval(open(DIR_SRC+'/version.py').read())


setup(
    name = 'uniseg',
    version = VERSION,
    author = 'Masaaki Shibata',
    author_email = 'mshibata@emptypage.jp',
    url = 'https://bitbucket.org/emptypage/uniseg-python',
    description\
        = 'A pure Python library to determine Unicode text segmentations',
    long_description = open('README').read(),
    license = 'MIT',
    packages = ['uniseg'],
    package_data = {
        'uniseg': ['ucd.sqlite3', 'docs/*.html', 'samples/*.py']
    },
    entry_points = {
        'console_scripts': ['uniseg-dbpath = uniseg.db:print_dbpath'],
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
    ],
    zip_safe = False,
)
