# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ''

setup(
    long_description=readme,
    name='lg-webos-cli',
    version='0.1.0',
    python_requires='==3.*,>=3.9.0',
    author='Tema Klochko',
    author_email='tema@klochko.ru',
    packages=['lg-webos-cli'],
    package_dir={"": "."},
    package_data={},
    install_requires=['pywebostv==0.*,>=0.8.4'],
)