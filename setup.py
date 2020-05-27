import re
import ast

from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('bkpads/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='bkpads',
    version=version,
    description='pyADS bridge for BK Precision 891 Python Library',
    url='https://github.com/jpunkt/bkpads.git',
    download_url='https://github.com/jpunkt/bk891/tarball/{0}'.format(version),
    license='MIT',
    author='Johannes Payr',
    author_email='johannes@arg-art.org',
    packages=[str('bkpads')],
    platforms='any',
    install_requires=['pyserial>=2.6']
)
