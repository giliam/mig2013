#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

moduleHMM = Extension('hmm', sources = ['hmmmodule.cpp'], libraries = ["boost_python"])
moduleFFT = Extension('fft', sources = ['fft.cpp'], libraries = ["boost_python"])

setup (name = 'MIG SE',
        version = '0.1',
        description = 'Package made for the SE MIG by first years at MINES ParisTech',
        ext_modules = [moduleHMM, moduleFFT])
