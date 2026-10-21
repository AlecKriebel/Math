#!/usr/bin/env python3
"""A polynomial denominator can pass a finite positive grid yet vanish inside.
This does not falsify the submitted theorem or its specific local diagnostic.
"""
from fractions import Fraction as Q
from math import prod
import json

def P(x):return prod((x-Q(i,7))**2 for i in range(7))
xstar=Q(1,14);K=Q(2)/P(xstar)
def D(x,y,z):return 1+2*x*z+3*y*z*z-K*P(x)
values=[D(Q(i,7),Q(j,7),Q(k,9)) for i in range(7) for j in range(7) for k in range(1,8)]
if min(values)<=0:raise RuntimeError('grid no longer strictly positive')
negative=D(xstar,Q(0),Q(1,9))
if negative!=Q(-62,63):raise RuntimeError('negative unsampled value changed')
print(json.dumps({'status':'PASS','grid_points':len(values),'minimum_grid_denominator':str(min(values)),'unsampled_point':[str(xstar),'0','1/9'],'unsampled_denominator':str(negative),'mechanism':'Phi=z+x*z^2+y*z^3-K*z*P(x), P(x)=product(i=0..6)(x-i/7)^2, K=2/P(1/14). Its vertical derivative is positive at every reviewer grid point and negative inside the grid box. Continuity forces a zero denominator between x=0 and x=1/14 at y=0,z=1/9.','claim_falsified':'Finite sampled positivity alone implies global nonsingularity','candidate_theorem_falsified':False},indent=2))
