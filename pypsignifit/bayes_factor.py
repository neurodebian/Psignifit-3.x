#!/usr/bin/env python

import numpy as np
from swignifit.swignifit_raw import vector_double
from pypsignifit import psignidata

__doc__ = """This module is intended to perform bayesian model comparison using model posterior probabilities

The rationale is the following:
Imaginge a number of candidate psychometric function models M1,M2,...Mn. We proceed by treating
M as another model parameter and perform gibbs sampling in the parameter space of this metamodel.
The function gibbs_model will then give the marginal posterior distribution in model space using gibbs sampling.
Interestingly, for this particular gibbs sampler, we can write out an analytical expression for the marginal stationary
distribution with respect to M. The function gibbs_analytical determines this marginal distribution.

In some applications, we might be interested in fitting more than one psychometric function in each
of the models to be compared. This is for example relevant if the feature that distinguishes between
the different models is e prior distribution. In this case, we can have each model consist of a sequence
of PsiInference objects.

Note that the logic of this module only works for Bayesian inference and *not* for a Bootstrap setting.
Also be aware that the data that were used for the different models should be the same across M1,M2,...,Mn.
"""

__all__ = ["gibbs_model","gibbs_analytical"]

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

def gibbs_analytical ( inference_objects ):
    """gibbs_analytical ( inference_objects )

    Analytically determine the marginal stationary distribution of M in the
    full model P(M,theta).

    :Parameters:
        *inference_objects* :
            psychometric function models to be compared. Note that these inference objects
            have to be based on the same data set in order to obtain valid results.
    """

    n = len ( inference_objects )
    T = np.zeros ( (n,n), 'd' )

    # Set up the transition matrix
    for k,M in enumerate ( inference_objects ):
        if isinstance ( M, psignidata.PsiInference ):
            M = [M]
        elif getattr ( M, "__iter__", False ):
            pass
        else:
            raise ValueError, "Elements of inference_objects should be either a PsiInference object or a sequence"

        for j in xrange ( M[0].mcestimates.shape[0] ):
            th = [ m.mcestimates[j] for m in M ]
            p =  np.exp ( np.array ( [ eval_post ( th, M_l ) for M_l in inference_objects ] ) )
            p /= p.sum()
            T[k] += p
        T[k] /= T[k].sum()

    # Now solve the stochastic matrix equation pi*T=pi
    A = (T-np.eye(n)).T
    A[0,:] = 1.
    p = np.zeros ( n, 'd' )
    p[0] = 1.

    return np.linalg.solve ( A, p ),T

def eval_post ( theta, M ):
    if isinstance ( M, psignidata.PsiInference ):
        M = [M]
    elif getattr ( M, "__iter__", False ):
        pass
    else:
        raise ValueError, "Elements of inference_objects should be either a PsiInference object or a sequence"

    return reduce ( lambda x,y: x+y, [ -m._pmf.neglpost ( th, m._data ) for th,m in zip(theta,M) ] )
