import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

install_requires = ['silabeador']


# This call to setup() does all the work
setup(
    name='fonemas',
    version='2.1.0',
    python_requires='>=3.6',
    description='Phonetic transcription of Spanish',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/fsanzl/fonemas',
    project_urls={
        'Source': 'https://github.com/fsanzl/fonemas/',
        'Tracker': 'https://github.com/fsanzl/fonemas/issues',
    },
    author='Fernando Sanz-Lázaro',
    author_email='fsanzl@gmail.com',
    license='LGPL',
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: Spanish',
    ],
    packages=['fonemas'],
    install_requires=['silabeador'],
    include_package_data=True,
)
