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
    name = 'sanitize',
    version = '0.0.2',
    author = 'Kal Sze (twitter.com/k_sze, github.com/ksze)',
    author_email = 'swordangel@gmail.com',
    description = 'A Python 2.7/3.2+ module to sanitize filenames in a (hopefully) cross-platform, cross-filesystem manner.',
    license = 'BSD',
    keywords = 'filename sanitization',
    url = 'https://github.com/ksze/sanitize',
    py_modules = ['sanitize'],
    long_description = read('README.md'),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
)
