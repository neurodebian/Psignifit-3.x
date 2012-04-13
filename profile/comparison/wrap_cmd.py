#!/usr/bin/env python

import re,os,sys

#  final: {alpha = 3.17655, beta = 0.769071, gamma = 0.5, lambda = 0.0225655}

fl = "-?\d+\.\d+e?-?\d?\d?"

parpattern = r"final:\s\{alpha = (%s), beta = (%s), gamma = 0.5, lambda = (%s)\}" % (fl,fl,fl)

#     D = 2.50996,  r_pd = 0.12849, r_kd = -0.300973

statspattern = r"D\s*=\s*(%s),\s*r_pd\s*=\s*(%s|nan),\s*r_kd\s*=\s*(%s|nan)" % ( fl,fl,fl )

def fit ( data, shape="Weibull" ):
    opts = """
#RUNS 0
#SHAPE %s
#LAMBDA_PRIOR -flat 0.0, 0.9999
    """ % (shape,)
    dat = ""
    for l in data:
        dat += "%g %g %d\n" % tuple(l)

    tmpfile = os.tmpnam()
    f = open ( tmpfile, "w" )
    f.write ( dat+opts )
    f.close()

    cin,cout = os.popen2 ( "psignifit %s" % tmpfile )
    cin.close()
    res = cout.read()

    # print res

    m = re.search ( parpattern, res )
    par = [float(x) for x in m.groups()]

    m = re.search ( statspattern, res )
    stat = [float(x) for x in m.groups()]

    return par,stat

def bootstrap ( data ):
    pass

if __name__ == "__main__":
    data = [[1.,.5,20],[2,.6,20],[3.,.75,20],[4.,.8,20],[5,.95,20],[6,1.,20],[7,.95,20]]
    print fit ( data )
