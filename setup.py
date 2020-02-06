"""`Dependency injector` setup script."""
import os
import re

from setuptools import setup, Extension


# Defining setup variables:
defined_macros = dict()
defined_macros['CYTHON_CLINE_IN_TRACEBACK'] = 0

# Getting description:
with open('README.rst') as readme_file:
    description = readme_file.read()

# Getting version:
with open('src/di/__init__.py') as init_file:
    version = re.search('__version__ = \'(.*?)\'', init_file.read()).group(1)


setup(name='di',
      version=version,
      description='Dependency injection library for Python',
      long_description=description,
      author_email='vlmihnevich@gmail.com',
      maintainer='Vitali Mikhnevich',
      maintainer_email='vlmihnevich@gmail.com',
      install_requires=[],
      packages=[
          'di',
      ],
      package_dir={
          '': 'src',
      },
      zip_safe=True,
      license='BSD New',
      platforms=['any'],
      keywords=[
          'Dependency injection',
          'DI',
          'Inversion of Control',
          'IoC',
          'Factory',
          'Singleton',
          'Design patterns',
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])

