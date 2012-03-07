#!/bin/bash

mex -cxx -I../../src/ mex_psignifit.cpp ../../src/bootstrap.cc ../../src/core.cc ../../src/data.cc ../../src/getstart.cc ../../src/integrate.cc ../../src/linalg.cc ../../src/mclist.cc ../../src/mcmc.cc ../../src/optimizer.cc ../../src/prior.cc ../../src/psychometric.cc ../../src/rng.cc ../../src/sigmoid.cc ../../src/special.cc
