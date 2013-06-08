from distutils.core import setup

from uniseg import __version__


setup(
    name = 'uniseg',
    version = __version__,
    author = 'Masaaki Shibata',
    author_email = 'mshibata@emptypage.jp',
    url = 'https://bitbucket.org/emptypage/uniseg-python',
    description = 'A pure Python module to determine Unicode text segmentation.',
    packages = ['uniseg'],
    package_data = {
        'uniseg': ['ucd.sqlite3'],
    },
    scripts = ['unibreak.py', 'uniwrap.py', 'wxwrapdemo.py'],
)
