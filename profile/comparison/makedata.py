#!/usr/bin/env python

import pypsignifit.psigobservers as obs
import cPickle

genprm = (4.,2.,.03)
shape = "logistic"

if shape == "Weibull":
    O = obs.Observer ( *genprm, core="poly", sigmoid="exponential" )
elif shape == "logistic":
    O = obs.Observer ( *genprm, core="ab", sigmoid="logistic" )

x = O.getlevels ( [.3,.4,.5,.6,.7,.99] )
datasets = []

for i in xrange ( 1000 ):
    datasets.append ( O.DoAnExperiment ( x, 20 ) )

cPickle.dump ( {'gen_par': genprm,'gen_shape': shape, 'dat':datasets}, open ( "data.pcl", "w" ) )
