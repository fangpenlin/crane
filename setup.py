from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name='docker-crane',
    version='0.1.0',
    description="A simple tool for building Dockerfiles",
    author='Victor Lin',
    author_email='bornstub@gmail.com',
    keywords='docker dockerfile build',
    url='http://github.com/victorlin/crane',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=[
        'jinja2',
        'click',
    ],
    entry_points={
        'console_scripts': ['crane = crane.commands:build']
    },
)
