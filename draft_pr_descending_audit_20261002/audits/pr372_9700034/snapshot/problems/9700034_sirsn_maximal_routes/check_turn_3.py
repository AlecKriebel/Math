#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import json
checks=laws=0
supports=[F(0),F(1,16),F(1,4),F(1,2),F(1)]
for weights in product(range(4),repeat=len(supports)):
 den=sum(weights)
 if not den:continue
 w=[F(x,den) for x in weights];a=sum(x*y for x,y in zip(w,supports));b=sum(x*y*y for x,y in zip(w,supports));p=sum(x for x,y in zip(w,supports) if y>0)
 assert a*a<=p*b;checks+=1
 if b:assert a*a/b<=p;checks+=1
 inv=sum(x/y for x,y in zip(w,supports) if y>0)
 assert p*p<=a*inv;checks+=1
 for n in [1,2,3,5,9,16]:
  sq=a/n+(1-F(1,n))*b
  assert sq-b==(a-b)/n;checks+=1
  if sq:assert (n*a)**2/(n*n*sq)<=p;checks+=1
  for m in [n,n+3,2*n]:
   sqm=a/m+(1-F(1,m))*b
   assert sq+sqm-2*sqm==(a-b)*(F(1,n)-F(1,m));checks+=1
  hit=1-sum(x*(1-y)**n for x,y in zip(w,supports))
  assert hit<=p;checks+=1
  if a+(n-1)*b:assert F(n)*a*a/(a+(n-1)*b)<=hit;checks+=1
 laws+=1
for s in range(1,41):
 assert F(2,s+2)<1;checks+=1
 for j in range(max(1,2*s),2*s+100):
  assert -j*j+(s-1)*j<=F(-j*j,2);checks+=1
for j in range(1,301):
 assert F(1,2**j)*(2**j)==1;checks+=1
for q in [F(1,2),F(1),F(2),F(3)]:
 for beta in range(9):
  for s in range(1,31):
   assert (s*q>beta+q+1)==((F(beta)-s*q)/(q+1)<-1);checks+=1
# Exact finite maxima for a truncated geometric environment; no simulation.
for J in range(1,31):
 assert sum(F(1,2**j)*2**j for j in range(1,J+1))==J;checks+=1
 assert sum(F(1,2**j) for j in range(1,J+1))==1-F(1,2**J);checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'finite_directing_laws':laws,'scope':'Exchangeable second moments, finite-maximum probability bounds, inverse-frequency Cauchy bound, radial/exponent identities and heavy-environment controls. No SIRSN realization.'},indent=2,sort_keys=True))
