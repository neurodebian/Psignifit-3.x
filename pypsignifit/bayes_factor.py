#!/usr/bin/env python

import numpy as np
from swignifit.swignifit_raw import vector_double

__doc__ = """This module """

def sample_model ( theta, inference_objects ):
    """sample_model ( theta, inference_objects )

    Sample a model from the full conditional f(M|theta)

    :Parameters:
    *theta* :
        list of arrays of parameters
    *inference_objects* :
        a sequence of inference objects to be sampled from.
    """
    p = np.zeros ( len(inference_objects), 'd' )
    th = [ vector_double ( th_ ) for th_ in theta ]
    for i,model in enumerate ( inference_objects ):
        if isinstance ( model, psignidata.PsiInference ):
            p[i] = -model._pmf.neglpost ( th[0], model._data )
        elif getattr ( inference_objects, "__iter__", False ):
            for M,th_ in zip ( model, th ):
                p[i] -= M._pmf.neglpost ( th_, M._data )
    p -= p.mean() # This should stabilize the exponential but should otherwise not change the result (constant factor)
    p = np.exp ( p )
    p /= np.sum ( p )
    return int ( np.where ( np.random.multinomial ( 1, p ) )[0] )

def sample_parameter ( inference_object ):
    """sample_parameter ( inference_object )

    reSample a single parameter setting from the model posterior.
    This is done by randomly selecting one of the samples stored in
    the inference object.

    :Parameters:
    *inference_object* :
        an inference object from which a parameter sample should be taken
    """
    if isinstance ( inference_object, psignidata.PsiInference ):
        i = np.random.randint ( len(inference_object.mcdeviance) )
        return [inference_object.mcestimates[i,:]]
    elif getattr ( inference_object, "__iter__", False ):
        out = []
        for model in inference_object:
            i = np.random.randint ( len(model.mcdeviance) )
            out.append ( model.mcestimates[i,:] )
        return out
    else:
        raise ValueError, "Incorrect input"


def gibbs_model ( inference_objects, nsamples=1000, M0=0 ):
    """gibbs_model ( inference_objects, nsamples=1000 )

    Perform Gibbs sampling in the full model P(M,theta).
    This function will return the marginal distribution across models.

    :Parameters:
    *inference_objects* :
        psychometric function models to be considered. Note that these inference objects
        have to be based on the same data set in order to obtain valid results.
        At the moment this is *not* checked!
    *nsamples* :
        how many samples are to be generated
    *M0* :
        Model to start with
    """

    mpost = np.zeros ( len(inference_objects), 'd' )
    chain = np.zeros ( nsamples )

    M = M0
    for i in xrange ( nsamples ):
        th = sample_parameter ( inference_objects[M] )
        M  = sample_model ( th, inference_objects )
        mpost[M] += 1
        chain[i] = M

    return mpost,chain
