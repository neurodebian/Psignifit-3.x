#!/usr/bin/env python
# encoding: utf-8
# vi: set ft=python sts=4 ts=4 sw=4 et:

######################################################################
#
#   See COPYING file distributed along with the psignifit package for
#   the copyright and license terms
#
######################################################################

""" Windows specific setup.py for Psignifit 3.x

Instead of linking to a shared library like in `setup.py`, all of Psi++ is
compiled into the extension.

"""

# other imports, metadata and extension definition
from setup import *

# Psi++ source files
psipp_sources = [
    "src/bootstrap.cc",
    "src/core.cc",
    "src/data.cc",
    "src/mclist.cc",
    "src/mcmc.cc",
    "src/optimizer.cc",
    "src/psychometric.cc",
    "src/rng.cc",
    "src/sigmoid.cc",
    "src/special.cc",
    "src/linalg.cc",
    "src/getstart.cc",
    "src/prior.cc",
    "src/integrate.cc"]

# swignifit interface, override the definition in `setup.py`
swignifit = Extension('swignifit._swignifit_raw',
        sources = psipp_sources + swignifit_sources,
        include_dirs=["src"])

if __name__ == "__main__":
    main(ext_modules=[swignifit])
