#!/usr/bin/env python3.2

classifiers = [
   "Development Status :: 5 - Production/Stable",
   "Environment :: Console",
   "Intended Audience :: Developers",
   "License :: OSI Approved :: Apache Software License",
   "Operating System :: OS Independent",
   "Programming Language :: Python :: 2.7",
   "Programming Language :: Python :: 3",
   "Programming Language :: Python :: 3.2",
   "Programming Language :: Python :: 3.3",
   "Topic :: Software Development :: Code Generators",
   "Topic :: Software Development :: Libraries :: Python Modules",
]

from distutils.core import setup


setup(
   name="3to2",
   packages=["lib3to2","lib3to2.fixes","lib3to2.tests"],
   entry_points={
      "console_scripts":[
         "3to2=lib3to2.main:main",
      ],
   },
   version="1.1.1",
   url="https://github.com/MaienM/lib3to2",
   author="Joe Amenta, Michon van Dooren",
   author_email="airbreather@linux.com, me@maienm.com",
   classifiers=classifiers,
   description="Refactors valid 3.x syntax into valid 2.x syntax, if a syntactical conversion is possible",
   long_description="",
   license="",
   platforms="",
)
