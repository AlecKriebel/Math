#!/usr/bin/env python3
"""Independent exact radial-family, isometric-span and nonattainment controls."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json
num=0

def ck(x):
 global num
 assert x
 num+=1

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(c,x):return tuple(c*z for z in x)
def radial(x,k):return scale((1+dot(x,x))**k,x)
def derivative(x,h,k):
 s=dot(x,x)
 if not k:return h
 return tuple((1+s)**k*v+2*k*(1+s)**(k-1)*dot(x,h)*u for u,v in zip(x,h))
# Different radial profiles from the submitted homogeneous cubic.
points=[tuple(map(Q,x)) for x in product((-1,0,1),repeat=3)]
radial_cases=0
for x in points:
 s=dot(x,x)
 for k in range(4):
  radial_cases+=1
  lam=(1+s)**k
  mu=lam if not k else lam+2*k*s*(1+s)**(k-1)
  ck(lam<=mu<=(1+2*k)*lam)
  ck(derivative(x,x,k)==scale(mu,x))
  h=(-x[1],x[0],Q(0))
  ck(dot(x,h)==0)
  ck(derivative(x,h,k)==scale(lam,h))
# Rational orthogonal frames embed every tested triple into a rotated R3.
for N in (7,11):
 v=tuple(Q(j+1) for j in range(N));vv=dot(v,v)
 def embed(x):
  z=x+(Q(0),)*(N-3)
  return sub(z,scale(2*dot(z,v)/vv,v))
 E=[embed(tuple(Q(i==j) for i in range(3))) for j in range(3)]
 for i,j in product(range(3),repeat=2):ck(dot(E[i],E[j])==int(i==j))
 for x in points:
  for k in range(4):ck(radial(embed(x),k)==embed(radial(x,k)))
 for x,y in product(points,repeat=2):
  ck(dot(sub(embed(x),embed(y)),sub(embed(x),embed(y)))==dot(sub(x,y),sub(x,y)))
  ck(dot(sub(radial(embed(x),2),radial(embed(y),2)),sub(radial(embed(x),2),radial(embed(y),2)))==dot(sub(radial(x,2),radial(y,2)),sub(radial(x,2),radial(y,2))))
# Exact integrated growth controls for rho(r)=r(1+r²)^k.
for r,R in product((Q(1,5),Q(1,2),Q(1),Q(2),Q(5)),repeat=2):
 if R<r:continue
 for k in range(4):
  ratio=R*(1+R*R)**k/(r*(1+r*r)**k)
  ck(R/r<=ratio<=(R/r)**(1+2*k))
# Diagonal ellipsoid in l2: all weights strictly between1 and2, neither end attained.
for N in range(1,41):
 weights=[v for k in range(N) for v in (1+Q(1,k+2),2-Q(1,k+2))]
 ck(all(1<w<2 for w in weights))
 ck(min(weights)==1+Q(1,N+1))
 ck(max(weights)==2-Q(1,N+1))
 ck(max(weights)/min(weights)<2)
 # Finite-support vectors test exact bounds; sequences of basis vectors give limits.
 z=[Q((-1)**k,k+1) for k in range(2*N)]
 nz=dot(z,z);Az=[w*x for w,x in zip(weights,z)]
 ck(nz<dot(Az,Az)<4*nz)
# Dimension-one counterexample, q=e^t>1: exact hyperbolic-function identity.
for q in map(Q,range(2,62)):
 sinh=(q-1/q)/2;sinh2=(q*q-1/(q*q))/2
 ck((sinh2-sinh)/sinh==q+1/q-1)
 ck(q+1/q-1>=q-1)
root=Path(__file__).resolve().parent
r={'verdict':'PASS','exact_assertions':num,'radial_profile_cases':radial_cases,'embedding_dimensions':[7,11],'method':'Independent rational controls for inhomogeneous radial profiles, orthogonal R3 embeddings, diagonal-ellipsoid nonattainment and sinh identity','artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),'limitations':['The Euclidean QC-to-QS theorem is an explicitly cited published input, not numerically certified.','The general nonradial Hilbert-space implication remains unresolved.','Finite-dimensional truncations do not establish infinite-dimensional compactness or attainment.']}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
