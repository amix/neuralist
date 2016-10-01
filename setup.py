#!/usr/bin/env python
# Copyright (c) 2007 Qtrac Ltd. All rights reserved.
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from setuptools import setup

setup(name='neuralist',
      version='0.51',
      author="amix",
      author_email="amix@doist.com",
      url="https://doist.com/",
      install_requires=[
          'redis>=2.10.0',
      ],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      packages=['neuralist'],
      include_package_data=True,
      zip_safe=False,
      platforms=["Any"],
      license="BSD",
      keywords='redis machien learning neural networks',
      description="A Python interface to access neural-redis."
)
