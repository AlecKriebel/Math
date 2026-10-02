#!/usr/bin/env python3
"""Finite exact checks of the physical spectral reduction's algebra; not a PDE simulation."""
from fractions import Fraction as Q
import json
count=0
def check(x):
    global count
    assert x
    count+=1

def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
for i in range(1,18):
 for j in range(1,19):
  for t in range(1,11):
   d=Q(t,7); k1=Q(i,5); k2=Q(j,9)
   p=[[1,d],[0,1]]; a=[[1,0],[2*k1,1]]; b=[[1,0],[2*k2,1]]
   c=mul(mul(mul(a,p),b),p); A=(1+d*k1)*(1+d*k2)
   check(c[0][0]*c[1][1]-c[0][1]*c[1][0]==1)
   check(c[0][0]+c[1][1]==4*A-2)
# A diagonal compact finite model: exact ratio error and the resolvent-derived estimate.
for den in range(3,22):
 for num in range(1,den-1):
  mu=Q(den-1,den); n=Q(num,den); r=(n+mu)/2
  for eps in (Q(-1,5),Q(1,3),Q(2,3)):
   for j in range(1,18):
    eta=mu**j+eps*n**j; nex=mu**(j+1)+eps*n**(j+1)
    check(nex-mu*eta==eps*n**j*(n-mu))
    check(eta!=0)
    if abs(eps)*(r/mu)**j<=Q(1,2):
     check(abs(nex/eta-mu)<=2*abs(eps)*(r+mu)*(r/mu)**j)
# Resonance determinant multiplication at rational values of the formal phase variable w.
for q,sigma in ((Q(1,4),Q(1,2)),(Q(2,7),Q(5,7)),(Q(3,8),Q(7,8))):
 for w in (Q(-3,2),Q(0),Q(1),1/q,Q(5,2)):
  check((1-q*w)*(1-sigma)==1-q*w-sigma+q*w*sigma)
 for j in range(1,70):
  u=q**j+sigma**j; nex=q**(j+1)+sigma**(j+1)
  check(nex/u-sigma==(q-sigma)*(q/sigma)**j/(1+(q/sigma)**j))
print(json.dumps({'status':'PASS','assertions':count,'coverage':['paraxial return determinant and trace','spectral observation quotient identities and bounds','same-resonance-set hidden-mode algebra'],'scope':'Exact finite algebra only; analytic/PDE assertions require the proofs and stated hypotheses in TURN_4.md.'},indent=2,sort_keys=True))
