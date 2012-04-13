#!/usr/bin/env python

import swignifit.swignifit_raw as sfr

def fit ( data, shape="weibull" ):
    nblocks = len(data)
    x = sfr.vector_double ( nblocks )
    k = sfr.vector_int ( nblocks )
    n = sfr.vector_int ( nblocks )
    for i in xrange ( nblocks ):
        x[i],p,n_ = data[i]
        n[i] = int(n_)
        k[i] = int(p*n[i])
    pdata   = sfr.PsiData ( x, n, k, 2 )

    if shape=="Weibull":
        sigmoid = sfr.PsiExponential () #sfr.PsiLogistic ()
        core    = sfr.polyCore ( pdata, sigmoid.getcode(), 0.1 ) #sfr.abCore ()
    elif shape=="logistic":
        sigmoid = sfr.PsiLogistic ()
        core    = sfr.abCore ()

    pmf     = sfr.PsiPsychometric ( 2, core, sigmoid )
    prior   = sfr.UniformPrior ( 0, .9999 )
    pmf.setPrior ( 2, prior )

    opt = sfr.PsiOptimizer ( pmf, pdata )
    par = opt.optimize ( pmf, pdata )
    devianceresiduals = pmf.getDevianceResiduals ( par, pdata )
    stat = [ pmf.deviance ( par, pdata ), pmf.getRpd ( devianceresiduals, par, pdata ), pmf.getRkd ( par, pdata) ]
    return par, stat

if __name__ == "__main__":
    data = [[1.,.5,20],[2,.6,20],[3.,.75,20],[4.,.8,20],[5,.95,20],[6,1.,20],[7,.95,20]]
    print fit ( data )
