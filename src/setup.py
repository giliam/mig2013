#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

module1 = Extension('hmm', sources = ['hmmmodule.cpp'], libraries = ["boost_python"])

setup (name = 'ContinuousMarkov',
        version = '0.1',
        description = 'Package made for the SE MIG by first years at MINES ParisTech',
        ext_modules = [module1])
