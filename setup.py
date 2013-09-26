#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(name='py_cbssports',
      description='Wrapper for the CBSSports RESTful API',
      author='Robert Buckley',
      author_email='rbuckley30@gmail.com',
      version='0.01',
      scripts=['ez_setup.py'],
      packages=['cbssports'],
      install_requires=['requests>=1.2.3'],
      )
