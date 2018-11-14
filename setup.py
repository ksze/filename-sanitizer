import os
from   setuptools import setup
import sys

if (
        (sys.version_info.major == 2 and sys.version_info.minor < 7) or
        (sys.version_info.major == 3 and sys.version_info.minor < 2)
    ):
    raise Exception('Python 2.7 or 3.2+ is required.')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'filename-sanitizer',
    version = '0.1.0',
    author = 'Kal Sze (twitter.com/k_sze, github.com/ksze)',
    author_email = 'swordangel@gmail.com',
    description = 'A Python 2.7/3.2+ package to sanitize filenames in a (hopefully) cross-platform, cross-filesystem manner.',
    license = 'BSD',
    keywords = 'filename sanitization',
    url = 'https://github.com/ksze/filename-sanitizer',
    packages = ['filename_sanitizer'],
    long_description = read('README.md'),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Filesystems',
    ],
)
