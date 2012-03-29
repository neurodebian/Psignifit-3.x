#!/bin/bash

# We assume that the shared object has been installed.
g++ -I../src -lpsipp -pg profile.cpp

# Run valgrind in verbose mode
valgrind --tool=callgrind -v ./a.out
