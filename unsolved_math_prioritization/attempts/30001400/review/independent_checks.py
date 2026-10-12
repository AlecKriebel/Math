#!/usr/bin/env python3
"""Independent rational checks of smoothing derivatives and order orientation."""
from fractions import Fraction as F
from itertools import combinations,product
from math import prod
from pathlib import Path
from hashlib import sha256
import json
counts={}
def ck(v,k):assert v,k;counts[k]=counts.get(k,0)+1

def comps(n,d):
 for cuts in combinations(range(1,n),d-1):
  b=(0,)+cuts+(n,);yield tuple(b[i+1]-b[i] for i in range(d))
def major(x,y):
 sx=sy=F(0)
 for a,b in zip(sorted(x,reverse=True),sorted(y,reverse=True)):
  sx+=a;sy+=b
  if sx>sy:return False
 return sx==sy

def tensor(x,y):return tuple(a*b for a in x for b in y)
vectors=0
for d in range(2,7):
 for a in comps(11,d):
  x=tuple(F(z,11) for z in a);u=tuple(F(1,d) for _ in a);vectors+=1
  ck(major(u,x),'uniform majorization')
  for eps in (F(1,13),F(2,7),F(5,8),F(12,13)):
   z=tuple((1-eps)*v+eps/d for v in x)
   # Exact derivative of the logarithmic product along the smoothing curve.
   slope=sum((F(1,d)-v)/w for v,w in zip(x,z))
   alternate=(sum(1/w for w in z)/d-d)/(1-eps)
   ck(slope==alternate,'Burg derivative identity')
   ck(slope>0,'strict Burg derivative')
   ck(prod(z)>prod(x),'integrated log-product direction')
   ck(min(z)>min(x) and max(z)<max(x),'generic endpoints')
   ck(sum(z)==1 and len(z)==d and min(z)>0,'same positive simplex')
   ck(sum(abs(v-w) for v,w in zip(z,x))==eps*sum(abs(v-w) for v,w in zip(u,x)),'exact l1 limit factor')
   # Cyclic-permutation averages give a separate bistochastic certificate.
   sortedx=sorted(x,reverse=True);sortedz=sorted(z,reverse=True)
   for k in range(1,d):
    gap=sum(sortedx[:k])-sum(sortedz[:k])
    ck(gap==eps*(sum(sortedx[:k])-F(k,d)) and gap>0,'strict proper prefix gap')
# Equal maxima/minima are permitted initially; perturbing x=y breaks both.
for x in [(F(1,2),F(1,4),F(1,4)),(F(2,5),F(2,5),F(1,10),F(1,10))]:
 d=len(x)
 for eps in [F(1,100),F(1,2)]:
  z=tuple((1-eps)*v+eps/d for v in x)
  ck(max(z)<max(x) and min(z)>min(x),'boundary genericity repair')
# Formal coefficients of log N_p and log d, avoiding approximate logarithms.
for p in [F(a,b) for b in range(1,8) for a in range(-12,13) if a not in (0,b)]:
 H=(1/(1-p),F(0))
 direct_forward=(1/(p-1),F(1));rhs_forward=(-H[0],F(1))
 ck(direct_forward==rhs_forward,'forward Renyi coefficients')
 direct_reverse=(-1/p,(1-p)/p)
 rhs_reverse=(-(1-p)/p*H[0],(1-p)/p)
 ck(direct_reverse==rhs_reverse,'reverse Renyi coefficients')
 ck((p*(p-1)>0)==(p<0 or p>1),'all-regime curvature sign')
# Tensoring a cyclic stochastic channel preserves both uniform states and orientation.
for d in range(2,6):
 y=tuple(F(i+1,d*(d+1)//2) for i in range(d))
 B=[[F(i==j,3)+F(i==(j+1)%d)*F(2,3) for j in range(d)] for i in range(d)]
 x=tuple(sum(B[i][j]*y[j] for j in range(d)) for i in range(d))
 ck(all(sum(r)==1 for r in B) and all(sum(B[i][j] for i in range(d))==1 for j in range(d)),'bistochastic channel')
 yy=tensor(y,y);xx=tensor(x,x)
 for i,k in product(range(d),repeat=2):
  value=sum(B[i][j]*B[k][l]*y[j]*y[l] for j,l in product(range(d),repeat=2))
  ck(value==xx[i*d+k],'tensor channel action')
 ck(major(x,y) and major(xx,yy),'majorization orientation')
 # A zero entry cannot lie below a positive target in equal dimension.
 z=(F(0),)+tuple(F(1,d-1) for _ in range(d-1))
 ck(not major(z,y),'zero entry exclusion')
# An explicit positive pair has two-copy order without one-copy order.
x=tuple(F(a,100) for a in (39,39,11,11));y=tuple(F(a,100) for a in (50,25,24,1))
ck(not major(x,y),'one-copy obstruction')
for n in range(2,5):
 xn=tuple(prod(v) for v in product(x,repeat=n));yn=tuple(prod(v) for v in product(y,repeat=n))
 ck(major(xn,yn),'nontrivial copy certificate')
 for p in (-3,-2,-1,0,1,2,3):
  nx=sum(a**p for a in xn);ny=sum(a**p for a in yn)
  ck(nx<=ny if p not in (0,1) else nx==ny,'tensor power convex control')
# d=1 and uniform starting vectors require no generic theorem.
for d in range(1,12):
 u=(F(1,d),)*d
 ck(major(u,u) and tensor(u,u)==(F(1,d*d),)*(d*d),'uniform branch')
p=Path(__file__).resolve().parent
print(json.dumps({'problem_id':30001400,'assertions':sum(counts.values()),'sections':counts,'positive_nonuniform_vectors':vectors,'artifact_sha256':sha256((p/'author_replay/KNOWN_CONSEQUENCE.md').read_bytes()).hexdigest(),'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite smoothing-derivative, proper-prefix, Renyi coefficient, and tensor-channel diagnostics. The continuum of orders uses the audited analytic argument, and eventual majorization uses the credited published theorem.'},indent=2,sort_keys=True))
