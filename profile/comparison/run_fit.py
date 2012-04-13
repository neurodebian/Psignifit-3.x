#!/usr/bin/env python

import cPickle
import wrap_cmd as cmd
import minimal_swig as sw
import pylab as pl

data = cPickle.load ( open ( "data.pcl" ) )

parameters_cmd = []
parameters_sw  = []

for d in data['dat']:
    d = pl.array(d)
    d[:,1] /= d[:,2]
    th_c,st_c = cmd.fit ( d, shape=data['gen_shape'] )
    th_s,st_s = sw.fit ( d,  shape=data['gen_shape'] )
    parameters_cmd.append ( th_c )
    parameters_sw.append ( th_s )

parameters_cmd = pl.array ( parameters_cmd )
parameters_sw  = pl.array ( parameters_sw  )
ok_cm = (parameters_cmd[:,0]<20) * (parameters_cmd[:,1]<20)
ok_sw = (parameters_sw[:,0]<20)  * (parameters_sw[:,1]<20)
print "CMD: %d, SWIG: %d" % (pl.sum(ok_cm),pl.sum(ok_sw))
ok = ok_cm*ok_sw
parameters_cmd = parameters_cmd[ok,:]
parameters_sw  = parameters_sw[ok,:]

pl.figure ( figsize=(10,10) )
for i in xrange ( 3 ):
    pl.subplot(311+i)
    pl.plot ( [data['gen_par'][i]]*2, [-1,2], 'k-' )
    jitter = 0.1*pl.randn(len(parameters_cmd[:,i]))
    lc = pl.plot ( parameters_cmd[:,i], jitter+1, 'r.' )
    ls = pl.plot ( parameters_sw[:,i],  jitter,   'b.' )
    pl.legend ( (lc,ls), (
        "cmd (%g)" % (pl.mean((parameters_cmd[:,i]-data['gen_par'][i])**2),),
        "swig (%g)" %(pl.mean((parameters_sw[:,i] -data['gen_par'][i])**2),) ) )

print "finished"
pl.savefig ( "%s_sim.pdf" % (data['gen_shape'],) )
pl.show()
