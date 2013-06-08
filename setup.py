from distutils.core import setup


setup(
    name = 'uniseg',
    version = '0.6.0',
    author = 'Masaaki Shibata',
    author_email = 'mshibata@emptypage.jp',
    url = 'https://bitbucket.org/emptypage/uniseg-python',
    description = 'A pure Python module to determine Unicode text segmentation',
    packages = ['uniseg'],
    package_data = {
        'uniseg': ['ucd.sqlite3'],
    },
    scripts = ['unibreak.py', 'uniwrap.py', 'wxwrapdemo.py'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing',
    ],
)
