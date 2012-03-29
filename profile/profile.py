#!/usr/bin/env python

import pypsignifit as psi
from pypsignifit.psigobservers import Observer
from numpy.random import uniform

O = Observer ( 4, 2, .03 )

x = uniform ( 1, 8, size=64 )
data = O.DoAnExperiment ( x, 20 )

B = psi.BootstrapInference ( data )
B.sample()

f = open ( "datafile.h", "w" )

for i,d in enumerate (data):
    f.write ( "x[%d] = %f; k[%d] = %d; n[%d] = %d;\n" % (i,d[0],i,d[1],i,d[2]) )

f.close()

psi.GoodnessOfFit ( B )
psi.show ()
