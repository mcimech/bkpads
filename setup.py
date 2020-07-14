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
        download_url='https://github.com/jpunkt/bkpads/tarball/{0}'.format(
            version),
        license='MIT',
        author='Johannes Payr',
        author_email='johannes.payr@mci.edu',
        platforms='any',

        packages=[
            'bkpads'
        ],

        install_requires=[
            'bkp891',
            'pyads',
            'click'
        ],

        entry_points='''
            [console_scripts]
            bkpads=bkpads:main
        '''

    )

