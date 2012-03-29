#!/usr/bin/env python

f = open ( "6_b_2_lo.txt" )
out = open ( "datafile.h", 'w' )

i = 0;
for l in f:
	x,p,n = [float ( y ) for y in l.split()]
	out.write ( "x[%d] = %f; k[%d] = %d; n[%d] = %d;\n" % (i,x,i,p*n,i,n) )
	i += 1
f.close()
out.close()
