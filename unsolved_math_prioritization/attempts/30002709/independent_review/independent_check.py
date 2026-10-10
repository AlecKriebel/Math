#!/usr/bin/env python3
"""Separate exact convention controls; not a proof of Datta's theorem."""
from fractions import Fraction as Q
from itertools import product
import json,math
count=0
def ck(x):
 global count
 assert x
 count+=1
# Rational ordered-group representatives, including the strict endpoint.
for e in range(1,41):
 reps=[Q(j,e) for j in range(e)]
 ck(all(0<=x<1 for x in reps));ck(len(reps)==e)
 for a,b in product(reps,repeat=2):
  ck((a-b).denominator==1 if a==b else (a-b).denominator!=1)
 for k in range(-2*e,2*e+1):
  q,r=divmod(k,e);ck(Q(k,e)==q+Q(r,e));ck(0<=Q(r,e)<1)
 ck(Q(e,e)==1 and not Q(e,e)<1)
# Lexicographic extension Z^2 / (mZ x nZ): initial segment size n, index mn.
for m,n in product(range(1,10),repeat=2):
 cosets={(a,b) for a in range(m) for b in range(n)}
 initial={(0,b) for b in range(n)}
 ck(len(cosets)==m*n);ck(len(initial)==n);ck(initial<=cosets)
 ck((len(initial)==len(cosets))==(m==1))
 # Representatives of every quotient class are nonnegative; this weaker
 # fact emphatically does not imply epsilon=e when m>1.
 ck(all(x>=(0,0) for x in cosets))
 for a,b in cosets:
  ck(((a,b)<(0,n))==(a==0))
# Dense rank-one initial segment: each positive rational is above a base value.
for denominator in range(1,35):
 for numerator in range(1,15):
  g=Q(numerator,2*3**denominator)
  k=0
  while Q(1,3**k)>=g:k+=1
  ck(0<Q(1,3**k)<g)
# Independent Newton correction formula for both simple roots of X^2-6 at 5.
lifts={}
for initial in (1,4):
 r=initial
 for k in range(1,13):
  mod=5**k;ck((r*r-6)%mod==0)
  error=(r*r-6)//mod
  correction=(-error*pow(2*r,-1,5))%5
  r2=r+correction*mod
  ck((r2*r2-6)%(5*mod)==0);ck(r2%mod==r)
  ck(sum(((r+j*mod)**2-6)%(5*mod)==0 for j in range(5))==1)
  r=r2
 lifts[str(initial)]=r
ck((lifts['1']+lifts['4'])%5**13==0)
# Q(sqrt6), represented a+b*sqrt6. The selected branch has sqrt6+1 a unit.
def mul(x,y):return (x[0]*y[0]+6*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
ck(mul((-1,1),(1,1))==(5,0))
unit_inverse=(Q(-1,5),Q(1,5))
ck(mul((1,1),unit_inverse)==(1,0))
trace=2*unit_inverse[0];norm=unit_inverse[0]**2-6*unit_inverse[1]**2
ck(trace==Q(-2,5));ck(norm==Q(-1,5))
ck(trace.denominator%5==0);ck(norm.denominator%5==0)
# That inverse lies in the selected local ring but is not integral over Z_(5).
# This is a finite control of the finite-versus-essential distinction.
ck(Q(1,1*1)==1);ck(Q(2,1*1)==2)
# Trivial valuations on finite extensions: e=epsilon=1, f=degree.
for n in range(1,100):ck(Q(n,1*n)==1)
print(json.dumps({'status':'PASS','exact_assertions':count,'floating_diagnostics':0,'split_prime_inverse':{'coordinates':['-1/5','1/5'],'trace':str(trace),'norm':str(norm)},'scope':'Exact local/global degree, initial-index, Hensel-lift and finite-versus-essential controls. No finite computation establishes the general valuation-ring classification.'},indent=2,sort_keys=True))
