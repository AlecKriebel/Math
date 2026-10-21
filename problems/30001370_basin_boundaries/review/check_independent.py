#!/usr/bin/env python3
"""Independent rational controls. Analytic arguments require the review."""
from fractions import Fraction as Q
from math import isqrt
import itertools,json
counts={}
def ck(cat,x):
 assert x,cat
 counts[cat]=counts.get(cat,0)+1
# A new 400-interval envelope (not the author's CSV).
worst=Q(0)
for j in range(400):
 a=Q(j,1000);b=a+Q(1,1000);be=(16-100*a*a)/(4-a*a)
 k=isqrt(be.numerator*10**12//be.denominator)
 if Q(k*k,10**12)<be:k+=1
 ck('interval',Q((k-1)**2,10**12)<be<=Q(k*k,10**12))
 bound=(2+b)**2/(4*(2-b)**2)*(1+Q(k,3*10**6)+be/4)
 ck('interval',bound<Q(91,100));worst=max(worst,bound)
# Direct weighted rank-one norm controls: arbitrary q, not only realizable means.
for q in itertools.product([Q(0),Q(1,3),Q(1)],repeat=3):
 for weights in [(Q(1,3),)*3,(Q(1,6),Q(1,3),Q(1,2))]:
  mean=sum(w*x for w,x in zip(weights,q))
  for beta in [Q(0),Q(1,4),Q(1),Q(9,4),Q(4)]:
   root={Q(0):Q(0),Q(1,4):Q(1,2),Q(1):Q(1),Q(9,4):Q(3,2),Q(4):Q(2)}[beta]
   C=1+root/3+beta/4
   for v in itertools.product([-1,0,1],repeat=3):
    ev=sum(w*x for w,x in zip(weights,v));tv=[x-beta*y*ev/(1+beta*mean) for x,y in zip(v,q)]
    ck('rank_one',sum(w*x*x for w,x in zip(weights,tv))<=C*sum(w*x*x for w,x in zip(weights,v)))
# Möbius inverse and distortion rational-grid controls, both signs and endpoints.
for r in [Q(j,50) for j in range(-20,21)]:
 for x in [Q(j,40) for j in range(-20,21)]:
  z=((r+4)*x+r+1)/(2*r*x+2)
  inv=(2*z-r-1)/(r+4-2*r*z)
  fp=(4-r*r)/(2*(1+r*x)**2)
  ck('mobius',inv==x)
  ck('mobius',Q(0)<1/fp<=Q(3,4))
  ck('mobius',abs((1-4*x*x)/(4-r*r))<=Q(25,96))
  ck('distortion',abs(-2*r/(1+r*x))<=1)
  ck('distortion',abs(-2*r/(4-r*r)-2*x/(1+r*x))<=Q(35,24))
# Exact branch section on zero and nonzero output fibers.
for a,b,z in itertools.product(range(5),repeat=3):
 v=Q(a+b,2)
 qa=Q(a)/v if v else Q(1);qb=Q(b)/v if v else Q(1)
 ck('zero_fiber',qa+qb==2)
 ck('zero_fiber',qa*v==a and qb*v==b)
 ck('zero_fiber',(qa*z+qb*z)/2==z)
# Flat cumulative transports on [0,1]. Density is constant on four cells.
# The pushforward of H' dx is uniform; moments telescope exactly even with flats.
flat_cases=0
for raw in itertools.product(range(4),repeat=4):
 total=sum(raw)
 if not total:continue
 heights=[Q(4*x,total) for x in raw];ends=[Q(0)]
 for h in heights:ends.append(ends[-1]+h/4)
 ck('transport',ends[-1]==1)
 for degree in range(6):
  integral=sum((ends[i+1]**(degree+1)-ends[i]**(degree+1))/Q(degree+1) for i in range(4))
  ck('transport',integral==Q(1,degree+1))
 if 0 in raw:flat_cases+=1
# Independent polynomial functional calculation with exact integration.
def integ(c):return sum(v*Q(1,2)**(i+1)*(1-(-1)**(i+1))/Q(i+1) for i,v in enumerate(c))
f=[Q(0),-Q(3,20),Q(0),Q(1)]
pf=[Q(0),Q(3,160),Q(0),Q(1,8)]
ck('linear',integ(f)==0);ck('linear',integ([Q(0)]+f)==0);ck('linear',integ([Q(0)]+pf)==Q(1,320))
for B in range(7,17):
 lam=Q(1,2)+Q(B,12)
 ck('linear',Q(1,12)/(1-Q(1,2)/lam)==lam/B)
 ck('linear',1+Q(B)/(2*lam-1)==7)
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'categories':counts,'independent_interval_count':400,'maximum_squared_envelope':str(worst),'flat_transport_cases':flat_cases,'scope':'Finite rational controls corroborate formulas and an independently covered contraction bound; the full theorem rests on the analytic audit.'},indent=2,sort_keys=True))
